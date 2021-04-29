import pathlib, datetime, os

_instance = None


class Logger:
    
    
    LOG_LEVEL_FINE = 0
    LOG_LEVEL_CONFIG = 1
    LOG_LEVEL_WARNING = 2
    LOG_LEVEL_SEVERE = 3


    def __init__(self, level : int):
        self.__name = pathlib.Path("logs/log_{}".format(datetime.date.today()))
        if not(pathlib.Path("./logs").exists()) or not(pathlib.Path("./logs").is_dir()):
            os.mkdir("./logs")
        self.__log_level = level

    def set_log_level(self, level : int):
        self.__log_level = level

    def is_loggable(self, level : int):
        if level < self.__log_level:
            return False
        return True

    def __write_log(self,msg : str,designator : str):
        with open(self.__name,'a') as file:
            file.write('{} {} {}\n'.format(datetime.datetime.now().strftime("%H:%M:%S"),designator,msg))
            file.close()

    def fine(self,msg : str):
        if self.is_loggable(self.LOG_LEVEL_FINE):
            self.__write_log(msg,"---")

    def config(self,msg : str):
        if self.is_loggable(self.LOG_LEVEL_CONFIG):
            self.__write_log(msg,"-->")
    
    def warning(self,msg : str):
        if self.is_loggable(self.LOG_LEVEL_WARNING):
            self.__write_log(msg,"==>")

    def severe(self,msg : str):
        self.__write_log(msg,"!>>")


    @staticmethod
    def get_instance(lvl):
        global _instance
        if _instance == None:
            _instance = Logger(lvl)
        return _instance