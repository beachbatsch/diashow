from datetime import datetime

def writeLog(log_file_path, message, append=True):
    if (append == True):
        log_file = open(log_file_path, "a")
    else:
        log_file = open(log_file_path, "w")
    # tz = datetime.timezone.utc
    ft = "%Y-%m-%dT%H:%M:%S%z"
    t = datetime.now().strftime(ft)
    line = f"{t} --- " + str(message)
    log_file.write(line + "\n")
    log_file.close()