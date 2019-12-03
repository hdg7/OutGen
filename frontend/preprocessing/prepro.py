import sys
from z3 import *
import numpy
import os

sys.path.append(os.environ["EURY_HOME"])

from backend.visitors.cVisitors.OutputVisitor import OutputVisitor
import backend.generator.InputGenerator as InputGenerator
import backend.support.functions as functions
import backend.evaluators.UniformComparator as UniformComparator
import backend.visitors.cVisitors.manipulateMain as manipulateMain
from pycparser import parse_file,c_generator

filename=sys.argv[1]
functionName=sys.argv[2]
gen=c_generator.CGenerator()

print(filename)
print(functionName)

if functionName == 'main':
    maniMain=manipulateMain.MainManipulator(filename)
    maniMain.eliminateParams()
    maniMain.addGlobalParams()
    maniMain.addScanfParams()
    F=open(filename+".pre.c","w")
    F.write(gen.visit(maniMain.main))
    F.close()
    filename=filename+".pre.c"
    functionName='mainFake'
print(filename)
print(functionName)

visitor=OutputVisitor()

inputGen=InputGenerator.InputGenerator(filename,functionName)
F=open(filename+".ori.c","w")
for func in maniMain.otherFuncs:
    F.write(gen.visit(func))
F.write(gen.visit(inputGen.target))
F.close()

visitor.instrument(inputGen.target)
F=open(filename+".cbmc.c","w")
for func in maniMain.otherFuncs:
    F.write(gen.visit(func))
F.write(gen.visit(inputGen.target))
F.close()
