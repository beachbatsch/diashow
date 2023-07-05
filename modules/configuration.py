
import sys
from os import makedirs, path
from os.path import exists
from configparser import ConfigParser, NoSectionError


APP_FOLDER = sys.path[0]
CONFIG_FOLDER_NAME = ".conf" 
CONFIG_file_name = "config.yaml"
CONFIG_FOLDER_PATH = path.join(APP_FOLDER, CONFIG_FOLDER_NAME)
CONFIG_FILE_PATH = path.join(CONFIG_FOLDER_PATH, CONFIG_file_name)


class Configuration(object):
    __instance = None
    __config = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')
    

    def createFolders(self):
        if not exists(path.join(APP_FOLDER, self.getString("general", "list_folder_name"))):
            makedirs(path.join(APP_FOLDER, self.getString("general", "list_folder_name")))
        if not exists(path.join(APP_FOLDER, self.getString("general", "log_folder_name"))):
            makedirs(path.join(APP_FOLDER, self.getString("general", "log_folder_name")))
        if not exists(path.join(APP_FOLDER, self.getString("general", "lock_folder_name"))):
            makedirs(path.join(APP_FOLDER, self.getString("general", "lock_folder_name")))
        if not exists(path.join(APP_FOLDER, self.getString("general", "res_folder_name"))):
            makedirs(path.join(APP_FOLDER, self.getString("general", "res_folder_name")))
        

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__instance.writeDefaultConfig()
            cls.__instance.readConfig()
            cls.__instance.createFolders()
        return cls.__instance


    def writeDefaultConfig(self):
        if not path.exists(CONFIG_FOLDER_PATH):
            makedirs(CONFIG_FOLDER_PATH)


        # Check if there is already a configurtion file
        if exists(CONFIG_FILE_PATH) == False:
            # Create the configuration file as it doesn't exist yet
            cfgfile = open(CONFIG_FILE_PATH, 'w')

            # Add content to the file
            self.__config = ConfigParser()

            self.__config.add_section('general')
            self.__config.set('general', 'images_to_show_folder_path', "/home/dshow/Bilder/")
            self.__config.set('general', 'list_folder_name', ".lists")
            self.__config.set('general', 'log_folder_name', ".logs")
            self.__config.set('general', 'lock_folder_name', ".locks")
            self.__config.set('general', 'res_folder_name', ".res")
            self.__config.set('general', 'diashow_app_name', 'feh')

            self.__config.add_section('scheduler')
            self.__config.set('scheduler', 'lock_file_name', '.scheduler_run')
            self.__config.set('scheduler', 'log_file_name', 'scheduler.log')
            self.__config.set('scheduler', 'intervall_in_seconds', '10')

            self.__config.add_section('synchronize')
            self.__config.set('synchronize', 'src_folder_path', '/mnt/iserv/')
            self.__config.set('synchronize', 'lock_file_name', '.synchronizing')
            self.__config.set('synchronize', 'log_file_name', 'synchronizations.log')
            self.__config.set('synchronize', 'fill-in_image_name', 'fill-in.jpg')
            self.__config.set('synchronize', 'src_list_file_name', 'src.list')
            self.__config.set('synchronize', 'dst_list_file_name', 'dst.list')
        
            self.__config.add_section('safestart')
            self.__config.set('safestart', 'lock_file_name', '.safestart_diashow')
            self.__config.set('safestart', 'log_file_name', 'safestart_diashow.log')
        
            self.__config.add_section('wall-e')
            self.__config.set('wall-e', 'lock_file_name', '.wall-e')
            self.__config.set('wall-e', 'log_file_name', 'wall-e.log')
            self.__config.set('wall-e', 'duration_in_days', '30')
            self.__config.set('wall-e', 'message_file_name', 'wall-e_message.txt')
            self.__config.set('wall-e', 'prefix_message_date', 'Erstellt am ')
            self.__config.set('wall-e', 'prefix_message_duration', 'Dieser Ordner inklusive der Dateien wird in ')

            self.__config.write(cfgfile)
            cfgfile.close()


    def readConfig(self):
        cfgfile = open(CONFIG_FILE_PATH, 'r')
        self.__config = ConfigParser()
        self.__config.read_file(cfgfile)
        return self.__config
    
        
    def getString(self, section, option):
        try:
            return self.__config.get(section, option)
        except NoSectionError as e:
            return "NoSectionError for section '{section}' and option '{option}'".format(section=section, option=option)
    
    def getInt(self, section, option):
        return self.__config.getint(section, option)
    
    def getLockFilePath(self, section):
        return path.join(APP_FOLDER, self.getString("general", "lock_folder_name"), self.getString(section, "lock_file_name"))

    def getLogFilePath(self, section):
        return path.join(APP_FOLDER, self.getString("general", "log_folder_name"), self.getString(section, "log_file_name"))
    
    def getFillInImageFilePath(self):
        return path.join(APP_FOLDER, self.getString("general", "res_folder_name"), self.getString("synchronize", "fill-in_image_name"))

    def getWallEMessageFilePath(self):
        return path.join(APP_FOLDER, self.getString("general", "res_folder_name"), self.getString("wall-e", "message_file_name"))

    def getSrcListFilePath(self):
        return path.join(APP_FOLDER, self.getString("general", "list_folder_name"), self.getString("synchronize", "src_list_file_name"))
    
    def getDstListFilePath(self):
        return path.join(APP_FOLDER, self.getString("general", "list_folder_name"), self.getString("synchronize", "dst_list_file_name"))

# ------------------------------------------ testing area ---------------------------------------------
#config = Configuration.instance()
#config.instance().getFillInImageFilePath()
#print("intervall: " , config.getInt("scheduler", "intervall_in_seconds"))
#print("safestart lockfile_name: ", config.getString("safestart", "lock_file_name"))
#print("not existent: ", config.getString("another_section", "another_option"))
      