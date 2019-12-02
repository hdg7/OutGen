import sys
import pickle
import os

sys.path.append(os.environ["EURY_HOME"])

import backend.support.functions as functions
import backend.generator.OutputDrivenGenerator as genOut
import backend.visitors.cVisitors.manipulateMain as manipulateMain
import backend.tester.TesterMainPro as TesterMainPro
from pycparser import c_generator


def generate(parameters):
    genera=genOut.OutputDrivenGenerator(parameters["filename"],parameters["functionName"],parameters["fileZ3"])
    inputs=[]
    while len(inputs) <  parameters["totalInputs"]:
        inputVal,outVal=genera.generateInputDiv(2,10)
        if(inputVal != [] and inputVal != None):
            inputs.append(inputVal)
    return inputs
