from datetime import datetime
from os import listdir, walk
from os import path
from os import remove
from os import makedirs
from os.path import exists
from modules.configuration import Configuration as config
from modules import logging
from modules import locking
 
import sys
import shutil
import mimetypes

APP_FOLDER =  sys.path[0]
SRC_FOLDER_PATH =  config.getInstance().getString("synchronize", "src_folder_path")
IMAGES_TO_SHOW_FOLDER_PATH = config.getInstance().getString("general", "images_to_show_folder_path")

LOG_FILE_PATH = config.getInstance().getLogFilePath("synchronize")
LOCK_FILEPATH = config.getInstance().getLockFilePath("synchronize")

SRC_LIST_FILE_PATH = config.getInstance().getSrcListFilePath()
DST_LIST_FILE_PATH = config.getInstance().getDstListFilePath()


print ("<<<<<<<<<<<<< sync started >>>>>>>>>>>>>>")
# --------------------------- data collection ------------------------------        
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
        if file_path.find(".list") == -1:
            response.append(file_path)
    return response


def collectPathsAndWriteList(output_file_path, folder_to_read_path):
    try:
        file_paths = open(output_file_path, "w")

        for filepath in getFilteredFilepaths(folder_to_read_path):
            file_paths.write(filepath + "\n")
        
        file_paths.close()
    except Exception as e:
        print("exception occurred writing path file: " + str(e))


# --------------------------- cleanup destination ------------------------------

def getToDeletePaths():
    to_delete = []
    try:
        file_src_list = open(config.getInstance().getSrcListFilePath(), "r")
        file_dst_list = open(config.getInstance().getDstListFilePath(), "r")

        src_paths = file_src_list.read().splitlines()
        dst_paths = file_dst_list.read().splitlines()

        for dst_path in dst_paths:
            found = False
            for src_path in src_paths:
                rel_dst = getRelativePath(dst_path, IMAGES_TO_SHOW_FOLDER_PATH)
                rel_src = getRelativePath(src_path, SRC_FOLDER_PATH)
                if rel_dst == rel_src:
                    found = True
            
            if found == False:
                to_delete.append(dst_path)
    except Exception as e:
        print("exception occurred reading files: " + str(e))
    return to_delete


def getRelativePath(path, base):
    return path[len(base):]

def removeDeletedFiles():
    paths = getToDeletePaths()
    for path in paths:
        print("remove deleted file: ", path)
        remove(path)
# --------------------------- copy missing files ------------------------------         

def copyMissingFiles():
    try:
        file_src_list = open(config.getInstance().getSrcListFilePath(), "r")
        collectPathsAndWriteList(DST_LIST_FILE_PATH, IMAGES_TO_SHOW_FOLDER_PATH)
        file_dst_list = open(config.getInstance().getDstListFilePath(), "r")
        
        src_paths = file_src_list.read().splitlines()
        dst_paths = file_dst_list.read().splitlines()

        for src_path in src_paths:
            if isImage(src_path):
                found = False
                for dst_path in dst_paths:
                    rel_dst = getRelativePath(dst_path, IMAGES_TO_SHOW_FOLDER_PATH)
                    rel_src = getRelativePath(src_path, SRC_FOLDER_PATH)
                    if rel_dst == rel_src:
                        found = True
                if found == False:
                    rel_path = getRelativePath(src_path, SRC_FOLDER_PATH)
                    dst_path = path.join(IMAGES_TO_SHOW_FOLDER_PATH, rel_path)
                    print("copy missing file: ", src_path,  " --> ", dst_path)
                    folder=path.dirname(dst_path)
                    makedirs(folder,  exist_ok = True)
                    shutil.copyfile(src_path, dst_path)
    except Exception as e:
        print("exception occurred reading files: " + str(e))


def isImage(src_path):
    mime_type = mimetypes.guess_type(src_path)
    if mime_type[0].find("image") >= 0:
        return True
    return False

# --------------------------- delete empty folders --------------------------         
def deleteEmptyFoldersFromDst():
    deleteEmptyFolders(IMAGES_TO_SHOW_FOLDER_PATH)

def deleteEmptyFolders(path_abs):
    walklist = list(walk(path_abs))
    for path, _, _ in walklist[::-1]:
        if len(listdir(path)) == 0:
            if path != IMAGES_TO_SHOW_FOLDER_PATH:
                shutil.rmtree(path)

# ----------------------------- fill-in image -------------------------------
def preventEmptyImageFolder():
    try:
        file_paths = getFilepaths(IMAGES_TO_SHOW_FOLDER_PATH)
        image_found = False

        for file_path in file_paths:
            if isImage(file_path) == True:
                image_found = True
                break

        dst_path = path.join(IMAGES_TO_SHOW_FOLDER_PATH, config.getInstance().getString("synchronize", "fill-in_image_name"))
        if image_found == False:
            shutil.copyfile(config.getInstance().getFillInImageFilePath(), dst_path)
    except Exception as e:
        print("Exception occurred preventing empty image folder: " + str(e))
        pass



# -------------------- avoid starting without src-folder ------------------
print ("<<<<<<<<<<<<< synchronize started >>>>>>>>>>>>>>")
def existsSrcFolder():
    if exists(SRC_FOLDER_PATH):
        return True
    else:
        return False



if (existsSrcFolder()):
    if (locking.isLocked(LOCK_FILEPATH) == False):
        locking.lock(LOCK_FILEPATH)
        logging.writeLog(LOG_FILE_PATH,"synchronize - START", True)
        collectPathsAndWriteList(SRC_LIST_FILE_PATH, SRC_FOLDER_PATH)
        collectPathsAndWriteList(DST_LIST_FILE_PATH, IMAGES_TO_SHOW_FOLDER_PATH)
        removeDeletedFiles()
        copyMissingFiles()
        deleteEmptyFoldersFromDst()
        preventEmptyImageFolder()
        locking.unlock(LOCK_FILEPATH)
    else:
        print("sync is running")
        logging.writeLog(LOG_FILE_PATH,"locked", True)
else:
    logging.writeLog(LOG_FILE_PATH,"ABORT - missing sourcefolder")
  
deleteEmptyFoldersFromDst()  
print ("<<<<<<<<<<<<< sync finished >>>>>>>>>>>>>>")

