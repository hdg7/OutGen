## @package Eurystheus
#  Configuration module.
#
#  This singleton object contents the configuration file.
import configparser

class Configuration:

    class __Configuration:
        config = configparser.ConfigParser()

        def __init__(self, filename):
            self.filename = filename
            self.config.read(filename)
        def __str__(self):
            return repr(self) + self.filename
        
    instance = None
    def __init__(self, filename=""):
        if not Configuration.instance and filename!="":
            Configuration.instance = Configuration.__Configuration(filename)
        elif filename=="":
            Configuration.instance = Configuration.__Configuration("config.ini")

    def __getattr__(self, name):
        return getattr(self.instance, name)
    
    def ConfigSectionMap(self,section):
        dict1 = {}
        options = Configuration.instance.config.options(section)
        for option in options:
            try:
                dict1[option] = Configuration.instance.config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
