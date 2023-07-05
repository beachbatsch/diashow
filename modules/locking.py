# --------------------------- avoid memory leak -----------------------------
from datetime import datetime
from os import remove
from os.path import exists


def lock(lock_file_path):
    try:
        lock_file = open(lock_file_path, "w")
        ft = "%Y-%m-%dT%H:%M:%S%z"
        t = datetime.now().strftime(ft)
        line = f"gestartet: {t}"
        lock_file.write(line + "\n")
        lock_file.close()
    except Exception as e:
        print("Exception occurred locking file {lock_file_path} :::".format(lock_file_path = lock_file_path), str(e))

def unlock(lock_file_path):
    try:
        remove(lock_file_path)
    except Exception as e:
        print("Exception occurred unlocking file {lock_file_path} :::".format(lock_file_path = lock_file_path), str(e))

def isLocked(lock_file_path):
    if exists(lock_file_path):
        return True
    else:
        return False