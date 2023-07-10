from os import listdir
from os import walk
from shutil import rmtree


def deleteEmptyFolders(base_path, include_base_path):
    walklist = list(walk(base_path))
    for path, _, _ in walklist[::-1]:
        if len(listdir(path)) == 0:
            if path == base_path:
                if include_base_path == True:
                    rmtree(path)
            else:
                rmtree(path)