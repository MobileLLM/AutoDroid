import yaml
file_path = 'output/calendar/utg.yaml'
with open(file_path, 'r') as file:
    yaml_data_new = yaml.safe_load(file)
print(yaml_data_new['records'][0]['State'])