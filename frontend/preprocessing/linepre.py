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
import backend.support.compareSingle as compareSingle
import backend.generator.InputGenerator as gen
from backend.support.compareSingle import AnnotatedTree
from backend.visitors.cVisitors.instrumentSingle import instrumentation
from pycparser import parse_file,c_generator

def get_children(node):
 if isinstance(node, tuple):
  return(node[1].children())
 return(node.children())

#def get_label(node):
# if isinstance(node, tuple):
#  return(get_label(node[1]))
# return(type(node))

def get_label(node):
 return(node)


def label_dist(node1,node2):
 #node1.show() 
 #node2.show() 
 if(type(node1)!=type(node2)):
  return(1)
 if isinstance(node1, tuple) and isinstance(node2, tuple):
#  if(node1[0]!=node2[0]):
#   return(1)
  return(label_dist(node1[1],node2[1]))
 if node1.attr_names != node2.attr_names:
  return(1)
 for attr in node1.attr_names:
  if getattr(node1, attr) != getattr(node2, attr):
   return(1)
 return(0)


fileFix=sys.argv[1]
fileBug=sys.argv[2]
functionName=sys.argv[3]

if functionName == 'main':
    maniMainFix=manipulateMain.MainManipulator(fileFix)
    maniMainFix.eliminateParams()
    maniMainFix.addGlobalParams()
    maniMainFix.addScanfParams()
    genCode=c_generator.CGenerator()
    F=open(fileFix+".pre.c","w")
    F.write(genCode.visit(maniMainFix.main))
    F.close()
    fileFix=fileFix+".pre.c"
    maniMainBug=manipulateMain.MainManipulator(fileBug)
    maniMainBug.eliminateParams()
    maniMainBug.addGlobalParams()
    maniMainBug.addScanfParams()
    F=open(fileBug+".pre.c","w")
    F.write(genCode.visit(maniMainBug.main))
    F.close()
    fileBug=fileBug+".pre.c"
    functionName='mainFake'
#print(fileFix)
#print(fileBug)
#print(functionName)



genFix=gen.InputGenerator(fileFix,functionName)
genBug=gen.InputGenerator(fileBug,functionName)
genCode=c_generator.CGenerator()
dictio=compareSingle.simple_distance(genFix.target,genBug.target,get_children,get_label,label_dist)
filtered = [i for i in dictio if i[0]!='KEEP']
maxA=None
maxB=None
for elem in filtered:
 if(elem[1]=='A' and maxA==None):
  maxA=elem
 elif(elem[1]=='A' and maxA!=None and maxA[2] < elem[2]):
  maxA=elem
 elif(elem[1]=='B' and maxB==None):
  maxB=elem
 elif(elem[1]=='B' and maxB!=None and maxB[2] < elem[2]):
  maxB=elem
#print(maxA)
#print(maxB)
visitorFix=AssertVisitor()
visitorBug=AssertVisitor()
visitorFix.instrument(genFix.target,maxA[2])
visitorBug.instrument(genBug.target,maxB[2])

if visitorFix.has_instrumented(genFix.target) == True:
    F=open(fileFix+".L"+str(maxA[2])+".cbmc.c","w")
    if functionName == 'mainFake':
     for func in maniMainFix.otherFuncs:
      F.write(genCode.visit(func))
    F.write(genCode.visit(genFix.target))
    F.close()
    visitorFix.observedCopy(genFix.target)
    F=open(fileFix+".L"+str(maxA[2])+".test.c","w")
    if functionName == 'mainFake':
     for func in maniMainFix.otherFuncs:
      F.write(genCode.visit(func))
    F.write(genCode.visit(genFix.target))
    F.close()

    visitorBug.observedCopy(genBug.target)
    F=open(fileBug+".test.c","w")
    if functionName == 'mainFake':
     for func in maniMainBug.otherFuncs:
      F.write(genCode.visit(func))
    F.write(genCode.visit(genBug.target))
    F.close()

else:
    print("Error")
print("Line:"+str(maxA[2]))
