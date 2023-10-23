import json
with open('element_description.json') as file:
    element_descs = json.load(file)

from InstructorEmbedding import INSTRUCTOR
model = INSTRUCTOR('hkunlp/instructor-xl')

embedded_elements = {}
for app, app_data in element_descs.items():
    # embedded_elements[app] = {}
    embedded_app_data = {}
    for state_str, elements in app_data.items():

        embedded_app_data[state_str] = []
        for element in elements:
            print(app, state_str, element)
            if element:
                embedding = model.encode(element).tolist()
            else:
                embedding = None
            embedded_app_data[state_str].append(embedding)
    embedded_elements[app] = embedded_app_data

json_data = json.dumps(embedded_elements)

# 将JSON字符串写入文件
with open('embedded_elements_desc.json', 'w') as file:
    file.write(json_data)