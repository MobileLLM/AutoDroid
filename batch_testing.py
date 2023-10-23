import yaml
import os
from argparse import ArgumentParser

import csv

data = []
# Open the CSV file
with open('tasks.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in reader:
        # Access each column value using index
        data.append(row)

for app in data:
    apk_path, output_path = app[1], app[2]
    for task in range(3, len(app)):
        os.system('adb emu avd snapshot load snap_2023-07-03_20-14-08')
        bash = f'droidbot -task "{task}" -a "{apk_path}" -o "{output_path}" -is_emulator -keep_app -keep_env'
        os.system(bash)

# parser = ArgumentParser(prog="batch_runner")
# parser.add_argument(
#     "--config", default="configs/task.yaml", help="Tasks and apps to be collected"
# )
# args = parser.parse_args()

# with open(args.config, "r") as f:
#     data = yaml.safe_load(f)

# for dt in data:

#     os.system('adb emu avd snapshot load snap_2023-07-03_20-14-08')

#     task = dt["task"].replace('"',"'")
#     apk = dt["apk"]
#     output = dt["output"]
#     bash = f'droidbot -task "{task}" -a "{apk}" -o "{output}" -is_emulator -keep_app -keep_env'
#     os.system(bash)