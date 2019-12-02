import sys
from z3 import *
import numpy
import os

sys.path.append(os.environ["EURY_HOME"])

from backend.visitors.cVisitors.AssertVisitor import AssertVisitor
from backend.visitors.cVisitors.BlockCreatorElse import BlockCreator
import backend.generator.InputGenerator as InputGenerator
import backend.support.functions as functions
import backend.evaluators.UniformComparator as UniformComparator
import backend.visitors.cVisitors.manipulateMain as manipulateMain
import backend.visitors.cVisitors.manipulateFunc as manipulateFunc
from backend.visitors.cVisitors import BranchIdentifier
from pycparser import parse_file,c_generator,c_parser


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
    F.close()
    filename=filename+".pre.c"
    functionName='mainFake'
else:
    maniMain=manipulateFunc.FuncManipulator(filename,functionName)
print(filename)
print(functionName)
cleaner=BlockCreator()
visitor=AssertVisitor()

inputGen=InputGenerator.InputGenerator(filename,functionName)
vis=BranchIdentifier.BranchIdentifier()
cleaner.generic_visit(inputGen.target)

reparser=c_parser.CParser()
inputGen.target=reparser.parse(gen.visit(inputGen.target))

lines=vis.identifyLine((inputGen.target))
print(lines)
for line in lines:
    localTarget=copy.deepcopy(inputGen.target)
    visitor.instrument(localTarget,line)
    if visitor.has_instrumented(localTarget) == True:
        F=open(filename+".L"+str(line)+".cbmc.c","w")
        if maniMain != None:
            for func in maniMain.otherFuncs:
                F.write(gen.visit(func))
                F.write(";\n")
        F.write(gen.visit(localTarget))
        F.close()
        visitor.observedCopy(localTarget)
        F=open(filename+".L"+str(line)+".test.c","w")
        if maniMain != None:
            for func in maniMain.otherFuncs:
                F.write(gen.visit(func))
                F.write(";\n")
        F.write(gen.visit(localTarget))
        F.close()
    else:
        print("Error in Line " + str(line))

