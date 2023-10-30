# AutoDroid

## About
This repository contains the code for the system for the paper: [Empowering LLM to use Smartphone for Intelligent Task Automation](https://arxiv.org/abs/2308.15272).

For accessing the code specifically related to processing the dataset `DroidTask`, please visit the [DroidTask](https://github.com/MobileLLM/DroidTask) repository.

AutoDroid is implemented based on the [DroidBot](https://github.com/honeynet/droidbot/) framework.

## How to install
Make sure you have:

1. `Python` 
2. `Java`
3. `Android SDK`
4. Added `platform_tools` directory in Android SDK to `PATH`

Then clone this repo and install with `pip`:

```shell
git clone git@github.com:MobileLLM/AutoDroid.git
cd AutoDroid/
pip install -e .
```

[//]: # (If successfully installed, you should be able to execute `droidbot -h`.)

## How to use

1. Prepare:
    + If you want to test AutoDroid with the apps used in our paper, please download the `apk.zip` folder from [Google Cloud](https://drive.google.com/file/d/1KfSc78bauVJxMYduNXtyxb31VFGiDYSO/view?usp=share_link), and unzip it, and prepare a device or an emulator connected to your host machine via `adb`. 
    + If you want to test AutoDroid with other apps, please download the `.apk` file to your host machine, and prepare a device or an emulator connected to your host machine via `adb`. 
    + Prepare a GPT API key, and go to `tools.py`, replace the `os.environ['GPT_URL']` with your own API key.

2. Start:
   ```shell
   droidbot -a <path/to/.apk> -o <output/of/app> -task <your task> -keep_env -keep_app
   ```
   you can try the scripts in the ./scripts folder, and the tasks from the DroidTask are listed in [the form](https://docs.google.com/spreadsheets/d/1r2v9BtQ-Xlsc5tUIFZbkBodL07bqKcCnaaaYAJQnUHU/edit?usp=sharing).


3. Explore:
   
   The purpose of exploration is to generate app-specific memory that can be used to augment existing LLMs (by prompting or fine-tuning).
    + Note that we only support manual exploration in this repo. Automated exploration can be supported by integrating with other GUI crawling tools/strategies, which is not the main feature of this repo.
    + To collect the exploration memory of an app, use the following command:
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
    + `utg.yaml` and `added_element_descriptions.yaml` are used in the [DroidTask](https://github.com/MobileLLM/DroidTask) repo as the `utg.yaml` and the `<app>.yaml` in the navigation folder.


5. Collect new tasks manually:
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
 
## Known limitations

- The current implementation is not good at determining task completion.
- The task automation performance may be unstable due to the randomness of LLMs, the style/quality of app GUI and task descriptions, etc.
- It requires connecting to a host machine via adb, instead of a standalone on-device solution.

Welcome to contribute!

## Note

Note that AutoDroid is currently for research purpose only. It may perform unintended actions (e.g. modifying your account/settings). Please use at your own risk.

Enjoy!
