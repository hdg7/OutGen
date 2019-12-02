from pycparser import parse_file, c_generator
import cffi
from .DynamicTester import DynamicTester

class DynamicTesterWPath(DynamicTester):
    def testFunction(self,inputs):
        if not(self.loaded):
            self.loadTester()
        output=[]
        for inputVal in inputs:
            outputVal = eval("self.lib."+self.functionName+"("+','.join(str(x) for x in inputVal)+")")
            #print(outputVal)
            if outputVal == -1:
                output.append(1)
            else:
                output.append(1-1/(1+outputVal))
        return output

