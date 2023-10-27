# AutoDroid
## About
This repository contains the code for the system for the paper: [Empowering LLM to use Smartphone for Intelligent Task Automation](https://arxiv.org/abs/2308.15272).

For accessing the code specifically related to processing the dataset `DroidTask`, please visit the [DroidTaskToolBox](https://github.com/MobileLLM/DroidTask) repository.
## How to install
Make sure you have:

1. `Python` 
2. `Java`
3. `Android SDK`
4. Added `platform_tools` directory in Android SDK to `PATH`

Then clone this repo and install with `pip`:

```shell
git clone git@github.com:wenh18/AutoDroidSys.git
cd AutoDroidSys/
pip install -e .
```

[//]: # (If successfully installed, you should be able to execute `droidbot -h`.)

## How to use

1. Prepare:
    + If you want to test AutoDroid with explored memory mentioned in [our paper](https://arxiv.org/abs/2308.15272), please download the `apk.zip` folder from [Google Cloud](https://drive.google.com/file/d/1KfSc78bauVJxMYduNXtyxb31VFGiDYSO/view?usp=share_link), and unzip it.
    + If you want to test AutoDroid with any app, please download the `.apk` file to your host machine, and prepare a device or an emulator connected to your host machine via `adb`. 


2. Start DroidBot:
   ```shell
   droidbot -a <path/to/.apk> -o <output/of/app> -task <your task> -keep_env -keep_app
   ```
   you can try the scripts in the ./scripts folder, and the tasks from the DroidTask are listed in [the form](https://docs.google.com/spreadsheets/d/1r2v9BtQ-Xlsc5tUIFZbkBodL07bqKcCnaaaYAJQnUHU/edit?usp=sharing).


3. Explore:
    + Note that we only support exploring manually in this repo, and will support automatically exploring in the future. 
    + set your task as `'--manual'` in the above bash command. For example:
   ```shell
   droidbot -a <path/to/.apk> -o <output/of/app> -task '--manual' -keep_env -keep_app
   ```
    + After droidbot starts, given the description prompt of a UI, you can choose the ID of the button you want to click in this UI. For example, if you want to choose the button with the content description 'Sort by' in the following UI: 
    ```
    Current UI state:
    <input id=0>Search</input>
    <button id=1 label='Sort by'></button> 
    <button id=2 label='Add to favorites'></button>
    <button id=3 label='More options'></button>
    <button id=4>Internal</button>
    <button id=5>Alarms<br>0 items</button>
    <button id=6>Android<br>2 items</button> 
    ...
    UI element ID: 1 
    ```
    + After the app is explored, the yaml file of utg is recorded in `<output of app>/utg.yaml`. 
    + Then you can run:
    ```
    python memory/memory_builder.py --app <app_name> --utg_path <path to utg.yaml>
    ```
    + The processed app memory is stored in `<output of app>/added_element_descriptions.yaml`
    + `utg.yaml` and `added_element_descriptions.yaml` are used in [DroidTask repo](https://github.com/MobileLLM/DroidTask) as the `utg.yaml` and the `<app>.yaml` in the navigation folder.


4. Collect new tasks manually:
    + It is mainly the same with exploring, except that you should set the task to `'<your task>--manual'`, for example:
    ```shell
   droidbot -a <path/to/.apk> -o <output/of/app> -task 'create an event of laundry--manual' -keep_env -keep_app
   ```
    + If you want to choose a button, enter the `<id>` of it as mentioned above. If you want to edit an input box, you should enter `<id>, 'input_text'`, for example:
    ```
   Current UI state:
   <button id=0 text='Collapse'></button>
   <input id=1>Search…</input>
   <button id=2 text='Clear query'></button>
   <button id=3 text='Change view'></button>
    ...
    UI element ID: 1, 'input_text'
    ```
    + The trace of the task will be saved in `output/of/app/<your task>.yaml`
 
## Limitations

We find that AutoDroid could not determine whether a task has been completed in many cases, which will be fixed in our future works.

## Note

Note that AutoDroid is currently for research purpose only. It may perform unintended actions. Please use at your own risk.

Enjoy!