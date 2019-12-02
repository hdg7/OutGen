import sys
from z3 import *
import numpy
import os

sys.path.append(os.environ["EURY_HOME"])

from backend.visitors.cVisitors.AssertVisitor import AssertVisitor
import backend.generator.InputGenerator as InputGenerator
import backend.support.functions as functions
import backend.evaluators.UniformComparator as UniformComparator
import backend.visitors.cVisitors.manipulateMain as manipulateMain
from backend.visitors.cVisitors import BranchIdentifier
from pycparser import parse_file,c_generator

filename=sys.argv[1]
functionName=sys.argv[2]

print(filename)
print(functionName)
maniMain=None
gen=c_generator.CGenerator()
if functionName == 'main':
    maniMain=manipulateMain.MainManipulator(filename)
    maniMain.eliminateParams()
    maniMain.addGlobalParams()
    maniMain.addScanfParams()
    F=open(filename+".pre.c","w")
    F.write(gen.visit(maniMain.main))
    for func in maniMain.otherFuncs:
        F.write(gen.visit(func))
    F.close()
    filename=filename+".pre.c"
    functionName='mainFake'
print(filename)
print(functionName)
