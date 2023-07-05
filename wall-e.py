from datetime import datetime
from os import walk
from os import path
from os.path import exists
from modules.configuration import Configuration as config
from modules import locking
from modules import logging

import sys
import shutil

APP_FOLDER =  sys.path[0]
SRC_FOLDER_PATH =  config.getInstance().getString("synchronize", "src_folder_path")
MESSAGE_FILE_NAME = config.getInstance().getString("wall-e", "message_file_name")
DURATION_IN_DAYS = config.getInstance().getInt("wall-e", "duration_in_days")
PREFIX_MESSAGE_DATE = config.getInstance().getString("wall-e", "prefix_message_date")
PREFIX_MESSAGE_DURATION = config.getInstance().getString("wall-e", "prefix_message_duration")

LOG_FILE_PATH = config.getInstance().getLogFilePath("wall-e")
LOCK_FILEPATH = config.getInstance().getLockFilePath("wall-e")
WALLE_MESSAGE_FILE_PATH = config.getInstance().getWallEMessageFilePath()

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"



def __getAllFolders(directory):
    folder_paths = [] 
    for (root, dirs, files) in walk(directory):
        for dir_name in dirs:
            folder_path = path.join(root, dir_name)
            folder_paths.append(folder_path)
    return folder_paths


def __replaceStringInFile(file_path, str_to_replace, replacement):
    file = open(file_path, "r")
    lines = file.read().splitlines()

    for i in range(0, len(lines)):
        line = lines[i]
        if line.find(str_to_replace) >= 0:
            lines[i] = line.replace(str_to_replace, replacement)
    file.close()

    file = open(file_path, "w")
    for line in lines:
        file.write(line + "\n")
    file.close()


def __writeCreationDate(message_file_path):
    dt = datetime.now().strftime(DATETIME_FORMAT)
    __replaceStringInFile(message_file_path, "{creation_date}", dt)
    


def createMissingMessages(folders):
    for folder in folders:
        message_file_path = path.join(folder, MESSAGE_FILE_NAME)
        if exists(message_file_path) == False:
            shutil.copyfile(WALLE_MESSAGE_FILE_PATH, message_file_path)
            __writeCreationDate(message_file_path)


def __readCreationDate(message_file_path):
    file = open(message_file_path, "r")
    lines = file.read().splitlines()
    for line in lines:
        if line.find(PREFIX_MESSAGE_DATE) >= 0:
            datestring = line[len(PREFIX_MESSAGE_DATE):].strip()
            dt = datetime.strptime(datestring, DATETIME_FORMAT)
            return dt
    return None



def __replaceDuration(message_file_path, duration_in_days):
    file = open(message_file_path, "r")
    lines = file.read().splitlines()
    for i in range(0, len(lines)):
        line = lines[i]
        if line.find(PREFIX_MESSAGE_DURATION) >= 0:
            line_rest = line[len(PREFIX_MESSAGE_DURATION):].strip()
            line_rest = line_rest[line_rest.find(" "):].strip()
            lines[i] = PREFIX_MESSAGE_DURATION + " " + str(duration_in_days) + " " + line_rest
    file.close()

    file = open(message_file_path, "w")
    for line in lines:
        file.write(line + "\n")
    file.close()



def __writeDuration(message_file_path):
    now = datetime.now()
    creation_date = __readCreationDate(message_file_path)
    delta = now - creation_date
    duration = DURATION_IN_DAYS - delta.days

    __replaceDuration(message_file_path, duration)



def updateDurations(folders):
    for folder in folders:
        message_file_path = path.join(folder, MESSAGE_FILE_NAME)
        __writeDuration(message_file_path)


def __readDuration(message_file_path):
    file = open(message_file_path, "r")
    lines = file.read().splitlines()
    for i in range(0, len(lines)):
        line = lines[i]
        if line.find(PREFIX_MESSAGE_DURATION) >= 0:
            line_rest = line[len(PREFIX_MESSAGE_DURATION):].strip()
            duration = line_rest[:line_rest.find(" ")].strip()
            return int(duration)
    return None

def __deleteFolder(folder_path):
    shutil.rmtree(folder_path)

def checkDurations(folders):
    for folder_path in folders:
        message_file_path = path.join(folder_path, MESSAGE_FILE_NAME)
        duration = __readDuration(message_file_path)
        if duration <= 0:
            __deleteFolder(folder_path)

# -------------------- avoid starting without src-folder ------------------
print ("<<<<<<<<<<<<< wall-e started >>>>>>>>>>>>>>")
def existsSrcFolder():
    if exists(SRC_FOLDER_PATH):
        return True
    else:
        return False



if (existsSrcFolder()):
    if (locking.isLocked(LOCK_FILEPATH) == False):
        locking.lock(LOCK_FILEPATH)
        logging.writeLog(LOG_FILE_PATH,"wall-e - START", True)
        folders = __getAllFolders(SRC_FOLDER_PATH)
        createMissingMessages(folders)
        updateDurations(folders)
        checkDurations(folders)
        locking.unlock(LOCK_FILEPATH)
    else:
        print("wall-e is running")
        logging.writeLog(LOG_FILE_PATH,"locked", True)
else:
    logging.writeLog(LOG_FILE_PATH,"ABORT - missing sourcefolder")

print ("<<<<<<<<<<<<< wall-e finished >>>>>>>>>>>>>>")


