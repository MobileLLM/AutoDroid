import os
import re
import hashlib
import ast
ACTION_MISSED = None

def get_id_from_view_desc(view_desc):
    '''
    given a view(UI element), get its ID
    '''
    return int(re.findall(r'id=(\d+)', view_desc)[0])
    # if view_desc[0] == ' ':
    #     view_desc = view_desc[1:]
    # view_desc_list = view_desc.split(' ', 2)
    # if len(view_desc_list) > 2:
    #     if view_desc_list[2][:6] != 'class=' and view_desc_list[2][:8] != 'checked=' :  # for example: <p id=10>Up time</p>
    #         new_view_desc_list = view_desc.split(' ', 1)
    #         latter_part = new_view_desc_list[1].split('>', 1)
    #         return int(latter_part[0][3:])
    #     else:  # for example, <button id=3 class='More options' checked=False></button>
    #         return int(view_desc_list[1][3:])
    # else:  # for example, <p id=4>June</p>
    #     latter_part = view_desc_list[1].split('>', 1)
    #     # print('************', view_desc, view_without_id)
    #     return int(latter_part[0][3:])
def insert_id_into_view(view, id):
    if view[0] == ' ':
        view = view[1:]
    if view[:2] == '<p':
        return view[:2] + f' id={id}' + view[2:]
    if view[:7] == '<button':
        return view[:7] + f' id={id}' + view[7:]
    if view[:6] == '<input':
        return view[:6] + f' id={id}' + view[6:]
    if view[:9] == '<checkbox':
        return view[:9] + f' id={id}' + view[9:]
    if view[:5] == '<span':
        return view[:5] + f' id={id}' + view[5:]
    import pdb;pdb.set_trace()

def get_view_without_id(view_desc):
    '''
    remove the id from the view
    '''
    id = re.findall(r'id=(\d+)', view_desc)[0]
    id_string = ' id=' + id
    return re.sub(id_string, '', view_desc)

def query_gpt(prompt):
    import requests
    URL = os.environ['GPT_URL']  # NOTE: replace with your own GPT API
    body = {"model":"gpt-3.5-turbo","messages":[{"role":"user","content":prompt}],"stream":True}
    headers = {'Content-Type': 'application/json', 'path': 'v1/chat/completions'}
    r = requests.post(url=URL, json=body, headers=headers)
    return r.content.decode()

def delete_old_views_from_new_state(old_state, new_state, without_id=True):
    '''
    remove the UI element in new_state if it also exists in the old_state
    '''
    old_state_list = old_state.split('>\n')
    new_state_list = new_state.split('>\n')
    old_state_list_without_id = []
    for view in old_state_list:
        view_without_id = get_view_without_id(view)
        if view[-1] != '>':
            view = view + '>'
        if view_without_id[-1] != '>':
            view_without_id = view_without_id + '>'
        old_state_list_without_id.append(view_without_id)
    customized_new_state_list = []
    for view in new_state_list:
        view_without_id = get_view_without_id(view)
        if view[-1] != '>':
            view = view + '>'
        if view_without_id[-1] != '>':
            view_without_id = view_without_id + '>'
        if view_without_id not in old_state_list_without_id: #or 'go back' in view or 'scroll' in view:
            if without_id:
                customized_new_state_list.append(view_without_id)
            else:
                customized_new_state_list.append(view)
    return customized_new_state_list


def get_item_properties_from_id(ui_state_desc, view_id):
    '''
    given the element id, get the UI element property from the state prompt
    '''
    # ui_state_desc = self.states[state_str]['raw_prompt']
    ui_state_list = ui_state_desc.split('>\n')
    for view_desc in ui_state_list:
        if view_desc[0] == ' ':
            view_desc = view_desc[1:]
        if view_desc[-1] != '>':
            view_desc += '>'
        id = get_id_from_view_desc(view_desc)
        if id == view_id:
            return get_view_without_id(view_desc)
    return ACTION_MISSED

def get_thought(answer):
    start_index = answer.find('Thought:') + len('Thought:')   # Find the location of 'start'
    if start_index == -1:
        start_index = answer.find('thought:') + len('thought:')
    if start_index == -1:
        start_index = answer.find('Thought') + len('Thought')
    if start_index == -1:
        start_index = answer.find('thought') + len('thought')
    if start_index == -1:
        start_index = 0
    end_index = answer.find('}')                   # Find the location of 'end'
    substring = answer[start_index:end_index] if end_index != -1 else answer[start_index:]
    return substring

def process_gpt_answer(answer):
    # pattern = r'(\d+\.)'
    # matches = re.findall(pattern, answer)
    # for match in matches:
    #     answer = answer.replace(match, '')
    answer = answer.replace('\n', ' ')
    return answer

def extract_gpt_answer(answer):
    split_answer = answer.split('4.')
    if len(split_answer) > 1:
        last_sentence = split_answer[1]
        pattern = r'id=(\d+)'
        match = re.search(pattern, last_sentence)
        try:
            id = int(match.group(0)[3:])
        except:
            id = re.search(r'\d+', last_sentence)
        return id
    else:
        return re.search(r'\d+', answer)

def make_prompt(task, ui_desc, history):
    introduction_prompt = "You are a smartphone assistant to help users complete tasks by interacting with mobile apps.\nGiven a task, the previous UI actions, and the content of current UI state, your job is to decide whether the task is already finished by the previous actions, and if not, decide which UI element in current UI state should be interacted."
    task_prompt = "Task: "
    history_prompt = "Previous UI actions: "
    interface_prompt = "Current UI state: "
    question_prompt = "Your answer should always use the following format:\n1. Completing this task on a smartphone usually involves these steps: <?>.\n2. Analyse the relations between the task and the previous UI actions and current UI state: <?>.\n3. Based on the analyses, is the task already finished? <Y/N>. The next step should be <?/None>.\n4. Can the task be proceeded with the current UI state? <Y/N>. Fill in the blank about next interaction: - id=<id/-1 for finished> - action=<tap/input> - input text=<text or N/A>"
    return introduction_prompt+'\n'+task_prompt + task + '\n' + history_prompt + '\n' + history + '\n' + interface_prompt +'\n'+ ui_desc + '\n' + question_prompt

def visualize_network(G):
    from pyvis.network import Network
    nt = Network('1500px', notebook=True, directed=True)
    nt.from_nx(G)
    nt.toggle_physics(True)
    nt.show('visualize/nx.html')


def extract_action(answer):
    llm_id = 'N/A'
    llm_action = 'tap'
    llm_input = "N/A"
    whether_finished_answer = re.findall(
        "3\.(.*)4\.", answer, flags=re.S
    )[0]
    for e in ["Yes.", "Y.", "y.", "yes.", "is already finished"]:
        if e in whether_finished_answer:
            llm_id = -1
            llm_action = "N/A"
            llm_input = "N/A"
            break
    finished_check = re.findall("4\.(.*)", answer, flags=re.S)[0]
    for e in [
        "No further interaction is required",
        "cannot be determined based on",
        "no further action is needed",
    ]:
        if e in finished_check:
            llm_id = -1
            llm_action = "N/A"
            llm_input = "N/A"
    if llm_id != -1:
        try:
            llm_id, llm_action, llm_input = re.findall(
                "- id=(N/A|-?\d+)(?:.|\\n)*-\s?action=(.+?)(?:\\n|\s)(?:.|\\n)*-\s*input text=\"?'?(N/A|\w+)\"?'?",
                answer,
            )[0]
            if llm_id == "N/A":
                llm_id = -1
            else:
                llm_id = int(llm_id)
            if "tapon" in llm_action.lower():
                llm_action = "tap"
            elif "none" in llm_action.lower():
                llm_action = "N/A"
            elif "click" in llm_action.lower():
                llm_action = "tap"
            assert llm_action in ["tap", "input", "N/A"]
        except:
            try:
                llm_id, llm_action = re.findall(
                    "-\s?id=(\d+).*-\s?action=(\w+)", answer, flags=re.S
                )[0]
                llm_id = int(llm_id)
                if (
                    "tapon" in llm_action.lower()
                    or "check" in llm_action.lower()
                    or "uncheck" in llm_action.lower()
                ):
                    llm_action = "tap"
                elif "none" in llm_action.lower():
                    llm_action = "N/A"
                assert llm_action in ["tap", "input", "N/A"]
            except:
                llm_id, llm_action, llm_input = eval(
                    input(
                        answer + "\nPlease input id, action, and text: "
                    )
                )
                llm_id = int(llm_id)
                llm_action = ["tap", "input", "N/A"][
                    int(llm_action)
                ]
                try:
                    if int(llm_input) == -1:
                        llm_input = "N/A"
                except:
                    pass
    return llm_id, llm_action, llm_input

def insert_onclick_into_prompt(state_prompt, insert_ele, target_ele_desc):

    def insert_onclick(statement, description):
        index = statement.find('>')
        inserted_statement = statement[:index] + f" onclick='{description}'" + statement[index:]
        return inserted_statement

    onclick_desc = 'go to complete the ' + target_ele_desc
    element_statements = state_prompt.split('>\n')
    elements_without_id = []
    for ele_statement in element_statements:
        ele_statement_without_id = get_view_without_id(ele_statement)
        if ele_statement_without_id[-1] != '>':
            ele_statement_without_id += '>'
        if insert_ele == ele_statement_without_id:
            ele_statement_without_id = insert_onclick(ele_statement_without_id, onclick_desc)

        elements_without_id.append(ele_statement_without_id)

    elements = []
    for id in range(len(elements_without_id)):
        elements.append(insert_id_into_view(elements_without_id[id], id))
    return '\n'.join(elements)

def hash_string(string):

    byte_string = string.encode()
    # Create a hash object using the SHA-256 algorithm
    hash_obj = hashlib.sha256(byte_string)
    # Get the hashed value as a hexadecimal string
    hashed_string = hash_obj.hexdigest()
    return hashed_string


if __name__ == '__main__':
    print(query_gpt('how can i cancel wechat charge'))
    # import openai
    #
    # openai.api_key = "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"  # 替换成你的API密钥
    #
    #
    # response = openai.Completion.create(
    #     engine="davinci",
    #     prompt="Translate the following English text to French: 'Hello, how are you?'",
    #     max_tokens=50
    # )
    #
    # print(response.choices[0].text.strip())
