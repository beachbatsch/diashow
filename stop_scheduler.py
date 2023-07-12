from os import path, remove, system
import sys
from modules.configuration import Configuration as config

APP_FOLDER = sys.path[0]
LOCK_FILEPATH = config.instance().getLockFilePath("scheduler")
DIASHOW_APP_NAME = config.instance().getString("general", "diashow_app_name")


def stopDiashow():
    cmd = "kill $(pidof /usr/bin/" + DIASHOW_APP_NAME + ")"
    system(cmd)

def unlock():
    try:
        remove(LOCK_FILEPATH)
    except Exception as e:
        #print("Exception occurred while unlocking: " + str(e))
        pass

stopDiashow()
unlock()