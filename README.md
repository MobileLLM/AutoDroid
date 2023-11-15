# AutoDroid

## About
This repository contains the code for the system for the paper: [Empowering LLM to use Smartphone for Intelligent Task Automation](https://arxiv.org/abs/2308.15272).

For accessing the dataset `DroidTask`, please visit the [DroidTask](https://github.com/MobileLLM/DroidTask_DataOverview) repository.

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


## Known limitations

- The current implementation is not good at determining task completion.
- The task automation performance may be unstable due to the randomness of LLMs, the style/quality of app GUI and task descriptions, etc.
- It requires connecting to a host machine via adb, instead of a standalone on-device solution.

Welcome to contribute!

## Note

Note that AutoDroid is currently for research purpose only. It may perform unintended actions (e.g. modifying your account/settings). Please use at your own risk.

Enjoy!
