# AutoDroid
## About
Paper: [Empowering LLM to use Smartphone for Intelligent Task Automation](https://arxiv.org/abs/2308.15272)
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
    + Note that we do not support randomly exploring an arbitrary app and generating memory, the code of which will be released soon.

2. Start DroidBot:
   ```shell
   droidbot -a <path\to\.apk> -o <output\of\app> -task <your task> -keep_env -keep_app
   ```
   you can try the scripts in the ./scripts folder, and the DroidTask are listed in [the form](https://docs.google.com/spreadsheets/d/1r2v9BtQ-Xlsc5tUIFZbkBodL07bqKcCnaaaYAJQnUHU/edit?usp=sharing)

## How to 

Note that AutoDroid is currently for research purpose only. It may perform unintended actions. Please use at your own risk.

Enjoy!