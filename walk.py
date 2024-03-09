import os
import fnmatch
import json
import yaml

all_state_strs = []

directory = './'

def find_json_files(directory):

    json_files = []  # 用来存放找到的JSON文件路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

directory_path = './'

json_files = find_json_files(directory_path)
for file in json_files:
    try:
        with open(file, 'r') as file:
            data = json.load(file)
        if 'state_str' in data.keys():
            all_state_strs.append(data['state_str'])
    except:
        print(file, 'wrong')
        continue
# import pdb;pdb.set_trace()
def load_yaml_files(directory):

    yaml_contents = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        yaml_contents[file_path] = yaml.safe_load(f)
                    except yaml.YAMLError as exc:
                        print(f"Error in loading {file_path}: {exc}")
    return yaml_contents


directory_path = './'


yaml_files_content = load_yaml_files(directory_path)
wrong_num = 0
right_num = 0

for path, content in yaml_files_content.items():
    if 'records' in content.keys():
        for step in content['records']:
            if isinstance(step['state_str'], str):
                if step['state_str'] not in all_state_strs:
                    
                    print(f'warning,', step['state_str'], 'original data missing')
                    wrong_num += 1
                else:
                    right_num += 1
                # print('str', step['state_str'])
            else:
                for state in step['state_str']:
                    for state_step in step['state_str']:
                        if state_step not in all_state_strs:
                            print(f'warning,', state_step, 'original data missing')
                            wrong_num += 1
                        else:
                            right_num += 1
                    
print(wrong_num, right_num)