

from os import path, remove, system
import sys
from modules.configuration import Configuration as config
from modules import locking

APP_FOLDER = sys.path[0]
LOCK_FILEPATH = config.instance().getLockFilePath("scheduler")
DIASHOW_APP_NAME = config.instance().getString("general", "diashow_app_name")


def stopDiashow():
    cmd = "kill $(pidof /usr/bin/" + DIASHOW_APP_NAME + ")"
    system(cmd)

print ("<<<<<<<<<<<<< stopDiashow started >>>>>>>>>>>>>>")
stopDiashow()
locking.unlock(LOCK_FILEPATH)
print ("<<<<<<<<<<<<< stopDiashow finished >>>>>>>>>>>>>>")
