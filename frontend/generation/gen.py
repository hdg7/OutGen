import sys
import pickle
import importlib

import os

sys.path.append(os.environ["EURY_HOME"])

import backend.generator.RandomInputGenerator as genFoc
import backend.tester.TesterMainPro as TesterMainPro
from pycparser import c_generator

#python3 ../../scripts/exp3.py /home/menendez/data/eurystheus/code/config.ini 13-A-14578281.c 13-A-14578265.c main 100
typeSimple=["rand"]
typeZ3=["dft","outgen","xorsample","greedyPareto","randPareto","basic","granular"]
typeExternal=["cavm"]

moduleClassMap={
    "dft":"DFTSPEA2Generator",
    "rand":"RandomInputGenerator",
    "greedyPareto":"DFTGreedyGenerator",
    "randPareto":"DFTRandomGenerator",
    "outgen":"DFTRandomGenerator",
    "xorsample":"DFTRandomGenerator",
    "basic":"BasicSolGenerator"
    }

def collectInputsNormal():
    parameters={}
    parameters["filename"]=sys.argv[2]
    parameters["fileOri"]=sys.argv[3]
    parameters["functionName"]=sys.argv[4]
    parameters["totalInputs"]=int(sys.argv[5])
    return parameters


def collectInputsSolver():
    parameters=collectInputsNormal()
    parameters["fileZ3"]=sys.argv[6]
    return parameters

def collectInputsExternal():
    parameters=collectInputsNormal()
    parameters["filenameHeader"]=sys.argv[6]
    return parameters

def dumpInputs(parameters,inputs):
    genFix=genFoc.InputGenerator(parameters["fileOri"],parameters["functionName"])
    with open(parameters["filename"] + ".inputs", "wb") as fp:
        pickle.dump(inputs, fp)

def createGenerator(moduleName):
    wModuleName='frontend.generation.' + moduleName
    print(wModuleName)
    return importlib.import_module(wModuleName)

moduleName = sys.argv[1]
generator=createGenerator(moduleName)
if(moduleName in typeSimple):
    parameters=collectInputsNormal()
elif(moduleName in typeZ3):
    parameters=collectInputsSolver()
else:
    parameters=collectInputsExternal()
inputs=generator.generate(parameters)
dumpInputs(parameters,inputs)
