import random
from ..configuration import Configuration
from subprocess import call
from ..support.functions import readPaths
import os.path
class CBMCConnector:
    
    def __init__(self,fileName,functionName):
        config=Configuration.Configuration()
        self.cbmc=config.ConfigSectionMap("CBMC")["path"]
        self.unwind=config.ConfigSectionMap("CBMC")["unwind"]
        self.options=config.ConfigSectionMap("CBMC")["options"]
        self.fileName=fileName
        self.functionName=functionName
        self.contraintsFile=functionName+"_"+ os.path.basename(fileName) + ".cvc"
    def createContraintsFile(self):
        debugFile = open("debugFile."+self.fileName+".log","w")
        print(self.fileName)
        print(self.functionName)
        call([self.cbmc,self.fileName,self.functionName,self.unwind,self.options,self.contraintsFile],stdout=debugFile)
        debugFile.close()

    def getConstraints(self):
        return readPaths(self.contraintsFile)
