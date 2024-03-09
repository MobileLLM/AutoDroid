# AutoDroid

## About
This repository contains the code for the system for the paper: [Empowering LLM to use Smartphone for Intelligent Task Automation](https://arxiv.org/abs/2308.15272).

For accessing the dataset `DroidTask`, you could download it from [Google Cloud](https://drive.google.com/file/d/1HcI3m3tLPaVr4aktvajBFur6zfULV0kh/view?usp=sharing), and you could refer to the [About Dataset Section](#About-Dataset). 

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
1.  Prepare:
    + If you want to test AutoDroid with the apps used in our paper, please download the `apk.zip` folder from [Google Cloud](https://drive.google.com/file/d/1KfSc78bauVJxMYduNXtyxb31VFGiDYSO/view?usp=share_link), and unzip it, and prepare a device or an emulator connected to your host machine via `adb`. 
    + If you want to test AutoDroid with other apps, please download the `.apk` file to your host machine, and prepare a device or an emulator connected to your host machine via `adb`. 
    + Prepare a GPT API key, and go to `tools.py`, replace the `os.environ['GPT_URL']` with your own API key.

2. Start:
   ```shell
   droidbot -a <path/to/.apk> -o <output/of/app> -task <your task> -keep_env -keep_app
   ```
   you can try the scripts in the ./scripts folder, and the tasks from the DroidTask are listed in [the form](https://docs.google.com/spreadsheets/d/1r2v9BtQ-Xlsc5tUIFZbkBodL07bqKcCnaaaYAJQnUHU/edit?usp=sharing).


## About Dataset

Organization of the Dataset, 
```
    DroidTask
    ├── applauncher
    │   ├── states
    │   │   ├── Screenshot 1.png
    │   │   ├── Screenshot 2.png
    │   │   ├── ...
    │   │   ├── View hierarchy 1.json
    │   │   ├── View hierarchy 2.json
    │   │   └── ...
    │   ├── task1.yaml
    │   ├── task2.yaml
    │   ├── ...
    │   └── utg.yaml
    ├── calendar
    │   ├── states
    │   │   ├── Screenshot 1.png
    │   │   ├── Screenshot 2.png
    │   │   ├── ...
    │   │   ├── View hierarchy 1.json
    │   │   ├── View hierarchy 2.json
    │   │   └── ...
    │   ├── task1.yaml
    │   ├── task2.yaml
    │   ├── ...
    │   └── utg.yaml
```
+ **DroidTask**: The top level of the dataset, containing folders for each application included in the DroidTask, such as `applauncher` and `calendar`.

+ **Application Folders**: Records all the screenshots and raw view hierarchy parsed by droidbot:

    + **States Folder**: This folder holds all the captured states of the application during usage. A state includes both visual representations (screenshots) and structural data (view hierarchies).

        + **Screenshots**: Images captured from the application's interface, named sequentially (e.g., `Screenshot 1.png`, `Screenshot 2.png`, etc.).

        + **View Hierarchies**: JSON files detailing the structure of the application's UI for each captured state (e.g., `View hierarchy 1.json`, `View hierarchy 2.json`, etc.).

    + **Task Files**: YAML files named `task1.yaml`, `task2.yaml`, etc., containing the ground truth data for specific tasks within the application.

    + **UTG File**: A `utg.yaml` file that records data from the user's random exploration of the application.

+ **Mapping Between Tasks and States**: If you want to use the screenshots in your method:

    + Each taski.yaml file (where i is the task number) references states through a state_str identifier.
    + This state_str can be matched with the state_str in a `view hierarchy k.json` file to associate tasks with their corresponding application states.
    + The name of the view hierarchy k.json file (where k is the state number) is also used to locate the corresponding screenshot, as the screenshot and view hierarchy files share the same naming convention.

## Known limitations

- The current implementation is not good at determining task completion.
- The task automation performance may be unstable due to the randomness of LLMs, the style/quality of app GUI and task descriptions, etc.
- It requires connecting to a host machine via adb, instead of a standalone on-device solution.

Welcome to contribute!

## Note

- We thank a lot for the wonderful open source apps from [Simple Mobile Tools](https://github.com/SimpleMobileTools).
- Note that AutoDroid is currently for research purpose only. It may perform unintended actions (e.g. modifying your account/settings). Please use at your own risk.

Enjoy!
