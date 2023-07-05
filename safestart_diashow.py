from os import walk
from os import path
from os import remove
from os import system
from os import makedirs
from os import fork
from os.path import exists
from pickle import TRUE
from time import sleep
from subprocess import run
from subprocess import PIPE
from datetime import datetime
from modules.configuration import Configuration as config
from modules import logging
from modules import locking
import sys
import psutil


APP_FOLDER = sys.path[0]
IMAGES_TO_SHOW_FOLDER_PATH = config.getInstance().getString("general", "images_to_show_folder_path")
DIASHOW_APP_NAME = config.getInstance().getString("general", "diashow_app_name")

DIASHOW_CMD = "/usr/bin/feh --auto-rotate --auto-zoom --fullscreen --hide-pointer --recursive --reload 60 --slideshow-delay 4 --sort mtime '" + IMAGES_TO_SHOW_FOLDER_PATH + "'"

LOG_FILE_PATH = config.getInstance().getLogFilePath("safestart")
LOCK_FILE_PATH = config.getInstance().getLockFilePath("safestart")

# ============================= DEFINITIONS ==============================
# -------------------- avoid starting with no images present  ------------------
def getFilepaths(directory):
    file_paths = [] 
    for (root, dirs, files) in walk(directory):
        for filename in files:
            filepath = path.join(root, filename)
            file_paths.append(filepath)
    return file_paths


def getFilteredFilepaths(directory):
    response = []
    file_paths = getFilepaths(directory)
    for file_path in file_paths:
        if file_path.find(".txt") == -1:
            response.append(file_path)
    return response

def existImages():
    for (root, dirs, files) in walk(IMAGES_TO_SHOW_FOLDER_PATH):
        for filename in files:
            if filename.lower().find(".jpg") >= 0 or filename.lower().find(".png") >= 0 or filename.lower().find(".jpeg"):
                return True
    return False


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

 

def startDiashowApp():
    pid=fork()
    if pid==0:
        # new process 
        system(DIASHOW_CMD) 


# ============================== ACTIONS ==============================
print ("<<<<<<<<<<<<< safestart started >>>>>>>>>>>>>>")
if existImages():
    if (locking.isLocked(LOCK_FILE_PATH) == False):
        locking.lock(LOCK_FILE_PATH)
        logging.writeLog(LOG_FILE_PATH, "safestart - START", True)
        if isDiashowAppRunning() == False:
            logging.writeLog(LOG_FILE_PATH, "app not running --> proceed starting app")
            startDiashowApp()
            logging.writeLog(LOG_FILE_PATH, "startDiashow called ")
        else:
            logging.writeLog(LOG_FILE_PATH, "app allready running") 
        locking.unlock(LOCK_FILE_PATH)
        logging.writeLog(LOG_FILE_PATH, "safestart - STOPPED", True)
    else:
        logging.writeLog(LOG_FILE_PATH, "locked", True)
else:
    logging.writeLog(LOG_FILE_PATH, "ABORT - missing images")
  
print ("<<<<<<<<<<<<< safestart finished >>>>>>>>>>>>>>")

