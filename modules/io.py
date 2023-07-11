from os import listdir
from os import walk
from os import remove
from os import path
from shutil import rmtree
import mimetypes


def getAllFolderPaths(directory, recursive=True):
    folder_paths = [] 
    for (root, dirs, files) in walk(directory):
        for dir_name in dirs:
            folder_path = path.join(root, dir_name)
            folder_paths.append(folder_path)
        if recursive == False:
            break
    return folder_paths


def deleteEmptyFolders(base_path, include_base_path):
    walklist = list(walk(base_path))
    for path, _, _ in walklist[::-1]:
        if len(listdir(path)) == 0:
            if path == base_path:
                if include_base_path == True:
                    rmtree(path)
            else:
                rmtree(path)


def deleteAllFilesInFolder(folder_path):
    file_paths = []
    for (dir_path, dir_names, file_names) in walk(folder_path):
        for file_name in file_names:
            file_path = path.join(dir_path, file_name)
            if path.isfile(file_path):
                file_paths.append(file_path)
        break
    for file_path in file_paths:
        remove(file_path)


def isImage(src_path):
    mime_type = mimetypes.guess_type(src_path)
    if mime_type[0].find("image") >= 0:
        return True
    return False
