import json
import os
import networkx as nx
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.embeddings import HuggingFaceInstructEmbeddings
import requests
import matplotlib.pyplot as plt
import ast
import numpy as np
import yaml
from tqdm import tqdm
import time
import hashlib
import tools

ACTION_MISSED = None

class Memory(object):
    """
    memory of the UI transition graph for autonomous agent
    """
    def __init__(self, app_name, app_output_path) -> None:
        self.app_name = app_name
        self.app_output_path = app_output_path #os.path.join('./output', self.app_name)
        self.nodes_and_edges = self.load_yaml_utg(update_state_strs=True)
        self.states, self.raw_memory_graph = self.build_manual_memory_graph()
    
    def get_first_state_str(self):  # TODO
        '''
        get the first state_str of the utg (the first screen of the app)
        '''
        utg = os.path.join(self.app_output_path, 'utg.yaml')
        with open(utg, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        if isinstance(data['records'][0]['state_str'], list):
            if len(data['records'][0]['state_str']) == 1:
                new_state_str = data['records'][0]['state_str'][0]
            else:
                new_state_str = self.hash_state(data['records'][0]['State'])
            return new_state_str
        else:
            return data['records'][0]['state_str']
    
    def load_yaml_utg(self, update_state_strs):  # TODO
        '''
        load the utg from utg.yaml
        '''
        utg = os.path.join(self.app_output_path, 'utg.yaml')
        with open(utg, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        
        # for super-states that contain many scrolled screens, hash the state_str into a string instead of the list
        if update_state_strs:
            for record_id in range(len(data['records'])):
                if isinstance(data['records'][record_id]['state_str'], list):
                    # print(data['records'][record_id]['state_str'])
                    if len(data['records'][record_id]['state_str']) == 1:
                        new_state_str = data['records'][record_id]['state_str'][0]
                    else:
                        new_state_str = self.hash_state(data['records'][record_id]['State'])
                    data['records'][record_id]['state_str'] = new_state_str
                    # print(new_state_str)
                # else:
                    # print(data['records'][record_id]['state_str'])
        return data
    
    def hash_state(self, state_prompt):
        return hashlib.sha256(state_prompt.encode()).hexdigest()
    
       
    def build_manual_memory_graph(self):  # TODO
        '''
        build the memory graph from the yaml file
        '''
        raw_memory_graph = nx.DiGraph()
        states = {}
        event_functions_dict = {}
        for record_id in range(len(self.nodes_and_edges['records'])):
            state_prompt = self.nodes_and_edges['records'][record_id]['State']
            state_str = self.nodes_and_edges['records'][record_id]['state_str']
            # print(record_id, state_str)
            # if state_str == '557aeea88606609eec93a428b50eb5a9dd2eedef1a07e1fdde83fafc1625022c':
            #     print(state_str, self.nodes_and_edges['records'][record_id+1]['state_str'])

            states[state_str] = {'raw_prompt': state_prompt}
            event_functions_dict[state_str] = {}

            event = self.nodes_and_edges['records'][record_id]['Choice']
            
            # build the memory graph
            if record_id < len(self.nodes_and_edges['records']) - 1:
                if raw_memory_graph.has_edge(state_str, self.nodes_and_edges['records'][record_id+1]['state_str']):
                    events = raw_memory_graph[state_str][self.nodes_and_edges['records'][record_id+1]['state_str']]['event']
                    if event not in events:
                        events.append(event)
                    raw_memory_graph.remove_edge(state_str, self.nodes_and_edges['records'][record_id+1]['state_str'])
                    # print(state_str, self.nodes_and_edges['records'][record_id+1]['state_str'], events)
                else:
                    events = [event]
                # if state_str == '557aeea88606609eec93a428b50eb5a9dd2eedef1a07e1fdde83fafc1625022c':
                #     print(state_str, self.nodes_and_edges['records'][record_id+1]['state_str'])
                raw_memory_graph.add_edge(state_str, self.nodes_and_edges['records'][record_id+1]['state_str'], event=events)
                                       
        return states, raw_memory_graph
    
    def _find_item_target_screen(self, current_state_str, view_id):
        '''
        given a state_str and a view's id, find the jumped state after clicking it
        '''
        successors_of_current_view = nx.dfs_successors(self.raw_memory_graph, source=current_state_str, depth_limit=1)
        for successor_str in successors_of_current_view:
            if self.raw_memory_graph.has_edge(current_state_str, successor_str):
                events = self.raw_memory_graph[current_state_str][successor_str]
                if view_id in events:
                    return successor_str
        return None  # we did not click or type this view, or doing so leads to the current_state_str back
    
    def _get_path_to_state(self, start_str, end_str):
        '''
        get the UI nodes and the action sequence that can lead to the state
        '''
        if nx.has_path(self.raw_memory_graph, start_str, end_str):
            path_nodes = nx.shortest_path(self.raw_memory_graph, start_str, end_str)
            action_nodes = [self.raw_memory_graph[path_nodes[i]][path_nodes[i+1]]['event'] for i in range(len(path_nodes) - 1)]#list(self.raw_memory_graph.edges(path_nodes, data=True))
            return path_nodes, action_nodes
        else:
            return None, None
    
    def _get_task_summary_by_gpt(self, state_str, state_items=None, target_item=None):
        all_task_paths = os.path.join(self.app_output_path, 'gpt_tasks')
        if state_items is None:
            task_path = os.path.join(all_task_paths, state_str+'.txt')
        else:
            task_path = os.path.join(all_task_paths, state_str+'_'+str(target_item)+'.txt')

        if os.path.exists(task_path):
            # tasks_list = np.load(task_path, allow_pickle=True).tolist()
            f = open(task_path, 'r')
            tasks = f.read()
            f.close()
            return tasks
        
        if state_items is None:
            ui_elements = self.states[state_str]['raw_prompt']#[136:]
            ui_element_num = ui_elements.count('\n')
        else:
            ui_element_num = len(state_items)
            ui_elements = '\n'.join(state_items)
            
        if ui_element_num < 1:
            print('warning: too few elements in this UI screen')
            tasks = ''
        else:
            # prefix_prompt = f'suppose you are using {self.app_name} app on a smartphone, the current UI screen has the following elements:\n'
            # prefix_prompt = f'suppose you are using {self.app_name} app on a smartphone, given a GUI screen described in html, please summarize the function of this UI screen in 1~3 sentences. Just return the function, do not tell me which button to click or which textbox to input, do not include \'go back to the front page\', or \'scroll up/down\' or any thing that you need to jump to another ui screen. Please ensure the summary is comprehensive, accurate, and concise'
            prefix_prompt = f"suppose you are using {self.app_name} app on a smartphone, given a GUI screen described in html, please summarize the function of this UI screen in some phrases with verb and noun. Just return the phrases, do not tell me which button to click or which textbox to input, do not include 'go back to the front page', or 'scroll up/down' or any thing that you need to jump to another ui screen.\n"
            
            
            example_request = f'For example:\nGUI:\n<button checked=True>No repetition</button>\n<button checked=False>Daily</button>\n<button checked=False>Weekly</button>\n<button checked=False>Monthly</button>\n<button checked=False>Yearly</button>\n<button checked=False>Custom</button>\n'
            example_summary = 'You should answer:\nSet the event reminder to non-recurring, daily, weekly, monthly, yearly and custom.\n'
            request_prompt = f'Now please summarize the function of this GUI screen:\n'
            state_prompt = f'GUI:\n{ui_elements}\n'
            query_prompt = 'please answer the phrases.\n'
            # note_prompt = 'Note that if there are a series of countries, place names, names, time, dates, or any semantically repetitive texts, summarize them in there category.'
            note_prompt = "Note that if there are a series of  countries, place names, names, time, dates, or any semantically repetitive sentence or words on buttons or texts, do not list them, summarize them in there category. Just return the phrases, do not tell me which button to click or which textbox to input, do not include 'go back to the front page', or 'scroll up/down' or any thing that you need to jump to another ui screen."
            prompt = prefix_prompt + example_request+example_summary+request_prompt+state_prompt+query_prompt+note_prompt
            print(prompt)

            tasks = tools.query_gpt(prompt)
            tasks = tools.process_gpt_answer(tasks)

        if not os.path.exists(all_task_paths):
            os.mkdir(all_task_paths)
        
        # with open(file_path, 'w') as f:
        #     json.dump()
        # np.save(task_path, tasks)
        f = open(task_path, 'w')
        f.write(tasks)
        f.close()

        return tasks
    
    def get_all_clickable_elements(self):
        '''
        get natrual language description for each actioned item on one screen
        '''
        item_functions = {}
        # for each state in the graph, extract the sub-graph, for each node in the sub-graph, get the action on the state (first action) that leads to the node, and add it to the item's function
        for state_id in tqdm(range(len(list(self.states.keys())))):
            
            state_str = list(self.states.keys())[state_id]
            state_prompt = self.states[state_str]['raw_prompt']

            item_functions[state_str] = {}

            state_successors_dict = nx.dfs_successors(self.raw_memory_graph, source=state_str, depth_limit=successor_depth)

            successor_new_items = {}
            
            # iterate over the successor state_strs
            for parent_node_str, successor_node_strs in state_successors_dict.items():

                path_nodes, path_actions = self._get_path_to_state(state_str, parent_node_str)

                if path_actions != []:  # the parent node is not the state_str itself 
                
                    first_actions = path_actions[0]
                    for first_action in first_actions:
                        if first_action not in successor_new_items.keys():
                            successor_new_items[first_action] = []

                for successor_str in successor_node_strs:  # add all the successor's items into the elements' descriptions
                    # filter out the items that have been in the root state
                    successor_items = tools.delete_old_views_from_new_state(old_state=state_prompt, new_state=self.states[successor_str]['raw_prompt'], without_id=True)
                    # print(successor_str, successor_items)
                    
                    # init the empty list for each element in the successor_new_items_dict
                    if path_actions == []:  # the parent node is not the state_str itself 
                        first_actions = self.raw_memory_graph[state_str][successor_str]['event']
                        for first_action in first_actions:
                            if first_action not in successor_new_items.keys():
                                successor_new_items[first_action] = []
                    print(first_actions, successor_str)
                    for successor_state_item in successor_items:
                        
                        if successor_state_item not in successor_new_items[first_actions[0]]:  # filter out the items that have been repeated
                            for first_action in first_actions:
                                successor_new_items[first_action].append(successor_state_item)

            for state_item, item2new_state_items in successor_new_items.items():
                print('***************************************************************************************')
                print(state_item, item2new_state_items)
                task = self._get_task_summary_by_gpt(state_str, item2new_state_items, target_item=state_item)
                item_functions[state_str][state_item] = task
                print('------------------------------------------------------------------------------')
                print(task)
        
            with open(dataset_path, 'w') as file:
                file.write(yaml.dump(item_functions, allow_unicode=True))
        return item_functions

    def get_nl_desc(self, successor_depth=1):
        '''
        get natrual language description for each actioned item on one screen
        '''
        dataset_path = os.path.join(self.app_output_path, 'added_element_descriptions.yaml')
        if os.path.exists(dataset_path):
            with open(dataset_path, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
            return data

        item_functions = {}
        # for each state in the graph, extract the sub-graph, for each node in the sub-graph, get the action on the state (first action) that leads to the node, and add it to the item's function
        for state_id in tqdm(range(len(list(self.states.keys())))):
            
            state_str = list(self.states.keys())[state_id]
            state_prompt = self.states[state_str]['raw_prompt']

            item_functions[state_str] = {}

            state_successors_dict = nx.dfs_successors(self.raw_memory_graph, source=state_str, depth_limit=successor_depth)

            successor_new_items = {}
            
            # iterate over the successor state_strs
            for parent_node_str, successor_node_strs in state_successors_dict.items():

                path_nodes, path_actions = self._get_path_to_state(state_str, parent_node_str)

                if path_actions != []:  # the parent node is not the state_str itself 
                
                    first_actions = path_actions[0]
                    for first_action in first_actions:
                        if first_action not in successor_new_items.keys():
                            successor_new_items[first_action] = []

                for successor_str in successor_node_strs:  # add all the successor's items into the elements' descriptions
                    # filter out the items that have been in the root state
                    successor_items = tools.delete_old_views_from_new_state(old_state=state_prompt, new_state=self.states[successor_str]['raw_prompt'], without_id=True)
                    # print(successor_str, successor_items)
                    
                    # init the empty list for each element in the successor_new_items_dict
                    if path_actions == []:  # the parent node is not the state_str itself 
                        first_actions = self.raw_memory_graph[state_str][successor_str]['event']
                        for first_action in first_actions:
                            if first_action not in successor_new_items.keys():
                                successor_new_items[first_action] = []
                    print(first_actions, successor_str)
                    for successor_state_item in successor_items:
                        
                        if successor_state_item not in successor_new_items[first_actions[0]]:  # filter out the items that have been repeated
                            for first_action in first_actions:
                                successor_new_items[first_action].append(successor_state_item)

            for state_item, item2new_state_items in successor_new_items.items():
                print('***************************************************************************************')
                print(state_item, item2new_state_items)
                task = self._get_task_summary_by_gpt(state_str, item2new_state_items, target_item=state_item)
                item_functions[state_str][state_item] = task
                print('------------------------------------------------------------------------------')
                print(task)
        
            with open(dataset_path, 'w') as file:
                file.write(yaml.dump(item_functions, allow_unicode=True))
        return item_functions
    

    def get_successor_by_node_edge(self, state_str, view_desc):
        '''
        given the state_str and the description of the view you click, predict the next string of screen it will jump to
        '''
        if view_desc[0] == ' ':
            view_desc = view_desc[1:]
        successors_dict = nx.dfs_successors(self.raw_memory_graph, source=state_str, depth_limit=1)
        for parent_node_str, successor_node_strs in successors_dict.items():
            for successor_node_str in successor_node_strs:
                path_nodes, edge_actions = self._get_path_to_state(state_str, successor_node_str)
                for edge_action_id in edge_actions[0]:
                    action_view_desc = tools.get_item_properties_from_id(self.states[state_str]['raw_prompt'], edge_action_id)
                    print(action_view_desc)
                    if action_view_desc == view_desc:
                        return successor_node_str
        return None
    

    def get_predictions_of_items(self, state_str):
        '''
        given a state_str, get all its successors, and find the items that was clicked to jump to the successor
        return:{item_desc1: successor1, ...}
        '''
        items_prediction_dict = {}
        all_items_description = self.get_nl_desc(1)

        if state_str not in list(all_items_description.keys()):
            return None

        state_items_descriptions = all_items_description[state_str]
        for item_id, item_function in state_items_descriptions.items():
            item_property = tools.get_item_properties_from_id(self.states[state_str]['raw_prompt'], item_id)
            items_prediction_dict[item_property] = item_function
        return items_prediction_dict

if __name__ == '__main__':

    # mem = Memory('filemanager',app_output_path='output/filemanager')
    mem = Memory('dialer',app_output_path='output/dialer')
    mem.get_nl_desc(1)
    # print(mem.get_successor_by_node_edge('e0d0c869524ad63e9df43ce8ed965e1b795181cdc9f9ca7891b7806aabd48a40', "<button class='Change view' checked=False></button>"))
    # print(mem.get_successor_by_node_edge('fcb3909d21bb7b0c8101b9b5747b1f24ba50c12570ac711b92a694a73606b753', "<button checked=False>Monthly view</button>"))
    import pdb;pdb.set_trace()
