# helper file of droidbot
# it parses command arguments and send the options to droidbot
import argparse
from droidbot import input_manager
from droidbot import input_policy
from droidbot import env_manager
from droidbot import DroidBot
from droidbot.droidmaster import DroidMaster


def parse_args():
    """
    parse command line input
    generate options including host name, port number
    """
    parser = argparse.ArgumentParser(description="Start DroidBot to test an Android app.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-d", action="store", dest="device_serial", required=False,
                        help="The serial number of target device (use `adb devices` to find)")
    parser.add_argument("-a", action="store", dest="apk_path", required=True,
                        help="The file path to target APK")
    parser.add_argument("-o", action="store", dest="output_dir",
                        help="directory of output")
    parser.add_argument("-task", action="store", dest="task", default="mingle around",
                        help="the task to execute, in natural language")

    parser.add_argument("-script", action="store", dest="script_path",
                        help="Use a script to customize input for certain states.")
    parser.add_argument("-count", action="store", dest="count", default=input_manager.DEFAULT_EVENT_COUNT, type=int,
                        help="Number of events to generate in total. Default: %d" % input_manager.DEFAULT_EVENT_COUNT)
    parser.add_argument("-interval", action="store", dest="interval", default=input_manager.DEFAULT_EVENT_INTERVAL,
                        type=int,
                        help="Interval in seconds between each two events. Default: %d" % input_manager.DEFAULT_EVENT_INTERVAL)
    parser.add_argument("-timeout", action="store", dest="timeout", default=input_manager.DEFAULT_TIMEOUT, type=int,
                        help="Timeout in seconds, -1 means unlimited. Default: %d" % input_manager.DEFAULT_TIMEOUT)
    parser.add_argument("-debug", action="store_true", dest="debug_mode",
                        help="Run in debug mode (dump debug messages).")
    parser.add_argument("-keep_app", action="store_true", dest="keep_app",
                        help="Keep the app on the device after testing.")
    parser.add_argument("-keep_env", action="store_true", dest="keep_env",
                        help="Keep the test environment (eg. minicap and accessibility service) after testing.")
    parser.add_argument("-grant_perm", action="store_true", dest="grant_perm",
                        help="Grant all permissions while installing. Useful for Android 6.0+.")
    parser.add_argument("-is_emulator", action="store_true", dest="is_emulator",
                        help="Declare the target device to be an emulator, which would be treated specially by DroidBot.")
    parser.add_argument("-accessibility_auto", action="store_true", dest="enable_accessibility_hard",
                        help="Enable the accessibility service automatically even though it might require device restart\n(can be useful for Android API level < 23).")
    parser.add_argument("-ignore_ad", action="store_true", dest="ignore_ad",
                        help="Ignore Ad views by checking resource_id.")
    options = parser.parse_args()
    # print options
    return options


def main():
    """
    the main function
    it starts a droidbot according to the arguments given in cmd line
    """
    opts = parse_args()
    import os
    if not os.path.exists(opts.apk_path):
        print("APK does not exist.")
        return

    droidbot = DroidBot(
        app_path=opts.apk_path,
        device_serial=opts.device_serial,
        task=opts.task,
        is_emulator=opts.is_emulator,
        output_dir=opts.output_dir,
        env_policy=env_manager.POLICY_NONE,
        policy_name=input_manager.POLICY_TASK,
        script_path=opts.script_path,
        event_interval=opts.interval,
        timeout=opts.timeout,
        event_count=opts.count,
        debug_mode=opts.debug_mode,
        keep_app=opts.keep_app,
        keep_env=opts.keep_env,
        grant_perm=opts.grant_perm,
        enable_accessibility_hard=opts.enable_accessibility_hard,
        ignore_ad=opts.ignore_ad)
    droidbot.start()


if __name__ == "__main__":
    main()
