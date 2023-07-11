import psutil
import sys
from datetime import datetime
from threading import Timer
from time import sleep
from os import fork, path, remove, system
from os import makedirs
from os.path import exists
from modules.configuration import Configuration as config
from modules import logging
from modules import locking

APP_FOLDER =  sys.path[0]

DIASHOW_APP_NAME = config.getInstance().getString("general", "diashow_app_name")
INTERVALL_IN_SECONDS = config.getInstance().getInt("scheduler", "intervall_in_seconds")

LOG_FILE_PATH = config.getInstance().getLogFilePath("scheduler")
LOCK_FILE_PATH = config.getInstance().getLockFilePath("scheduler")

SAFESTART_PY_CMD = "/usr/bin/python '" + path.join(APP_FOLDER, "safestart_diashow.py") + "'"
SYNCHRONIZE_PY_CMD = "/usr/bin/python '" + path.join(APP_FOLDER, "synchronize.py") + "'"
WALLE_PY_CMD = "/usr/bin/python '" + path.join(APP_FOLDER, "wall-e.py") + "'"


    

# ---------------- avoid starting diashow-app multiple times --------------
def isDiashowAppRunning():
    try: 
        for process in psutil.process_iter():
            if process.name() == DIASHOW_APP_NAME:
                return True
        return False
    except Exception as e:
        print("isDiashowAppRunning - EXCEPTION: " + str(e))
        return False
 

def startSafestartBash():
    system(SAFESTART_PY_CMD)  

def startSynchronizeBash():
    system(SYNCHRONIZE_PY_CMD)

def startWallE():
    system(WALLE_PY_CMD)




def hello(name):
    print ("Hello %s!" % name)


# ============================== ACTIONS ==============================
print ("<<<<<<<<<<<<< scheduler started >>>>>>>>>>>>>>")
logging.writeLog(LOG_FILE_PATH, "scheduler - START", True)
locking.lock(LOCK_FILE_PATH)

try:
    while(locking.isLocked(LOCK_FILE_PATH)):
        print("isDiashowAppRunning: ", isDiashowAppRunning())
        if (isDiashowAppRunning() == False):
            startSafestartBash()
        
        startSynchronizeBash()
        sleep(INTERVALL_IN_SECONDS)
        startWallE()
        sleep(INTERVALL_IN_SECONDS)
finally:
    locking.unlock(LOCK_FILE_PATH)

logging.writeLog(LOG_FILE_PATH, "scheduler - STOPPED", True)
print ("<<<<<<<<<<<<< scheduler finished >>>>>>>>>>>>>>")
