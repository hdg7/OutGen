import sys
import pickle
import random
from pydoc import locate
import os

sys.path.append(os.environ["EURY_HOME"])

import backend.support.functions as functions
import backend.generator.InputGenerator as genOut
import backend.visitors.cVisitors.manipulateFunc as manipulateFunc
import backend.tester.TesterMainPro as TesterMainPro
from pycparser import c_generator

#python3 ../../scripts/exp3.inputs.py 13-A-14578281.mut.1.c main inputs.txt

moduleClassMap={
    "sem":"TesterMainProTcas",
    "obs":"TesterMainPro",
    "semOut":"TesterMainProOutputTcas",
    "obsOut":"TesterMainProOutput",
    "obsState":"TesterMainProState"
    }

submoduleClassMap={
    "sem":"TesterMainPro",
    "obs":"TesterMainPro",
    "semOut":"TesterMainProOutputTcas",
    "obsOut":"TesterMainProOutput",
    "obsState":"TesterMainProState"
    }


def collectInputsNormal():
    parameters={}
    parameters["filename"]=sys.argv[2]
    parameters["functionName"]=sys.argv[3]
    parameters["inputsFile"]=sys.argv[4]
    if(len(sys.argv) > 5):
        parameters["totalInputs"]=int(sys.argv[5])
        parameters["seed"]=int(sys.argv[6])
    return parameters

def createTester(moduleAlias):
    wModuleName='backend.tester.' + moduleClassMap[moduleAlias] + '.' + submoduleClassMap[moduleAlias]
    print(wModuleName)
    return locate(wModuleName)


#This should be preprocessing
# if functionName == 'main':
#     maniMainBug=manipulateMain.MainManipulator(filenameBug)
#     maniMainBug.eliminateParams()
#     maniMainBug.addGlobalParams()
#     maniMainBug.addScanfParams()
#     gen=c_generator.CGenerator()
#     F=open(filenameBug+".pre.c","w")
#     F.write(gen.visit(maniMainBug.main))
#     F.close()
#     filenameBug=filenameBug+".pre.c"
#     functionName='mainFake'
# else:

moduleAlias = sys.argv[1]
parameters=collectInputsNormal()
maniMainBug=manipulateFunc.FuncManipulator(parameters["filename"],parameters["functionName"])

with open(parameters["inputsFile"], "rb") as fp:
     inputs = pickle.load(fp)

if len(sys.argv) > 4:
    random.seed(parameters["seed"])
    if(parameters["totalInputs"]>len(inputs)):
        finalInputs=inputs
    else:
        indexes=random.sample(range(len(inputs)),parameters["totalInputs"])
        finalInputs=[inputs[i] for i in indexes]
else:
    finalInputs=inputs


inputGeneratorBug =genOut.InputGenerator(parameters["filename"],parameters["functionName"])
tester=createTester(moduleAlias)
testerMutant = tester(inputGeneratorBug.target,parameters["functionName"],finalInputs)
testerMutant.addOtherFuncs(maniMainBug.otherFuncs)
testerMutant.dumpTests(parameters["filename"]+".cov.c")

