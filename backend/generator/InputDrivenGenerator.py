from pycparser import parse_file
from random import randint
from z3 import *
from ..support.functions import sub
from ..visitors.cVisitors.ReturnVisitor import ReturnVisitor
from ..visitors.cVisitors.LocalVisitor import LocalVisitor
from .InputGenerator import InputGenerator
import random
import copy

class OutputDrivenGenerator(InputGenerator):

    def __init__(self,fileName,functionName,filez3):
        InputGenerator.__init__(self,fileName,functionName)
        self.ctx = Context()
        self.f = parse_smt2_file(filez3,ctx=self.ctx)
        self.s=Solver(ctx=self.ctx)
        self.s.add(self.f)
        print(self.f)
        self.dicti={}
        self.varNames.remove('__out_var')
        for var in self.varNames:
            self.dicti["_start__"+str(var)+"_0_1"]=eval('Function("'+'_start__'+str(var)+'_0_1",BitVecSort(32,self.ctx))')
        self.dicti["_start____out_var_0_1"]=eval('Function("_start____out_var_0_1",BitVecSort(32,self.ctx))')
        self.dicti.update(globals())

        
    def generateInputs(self,total,num):
        count=0
        sols=[]
        expressions=[]
        while((count< total/2) and (len(sols)<total)):
            self.s.push()
            self.dicti['local_ctx']=self.ctx
            if(len(expressions)>0):
                for exp in expressions:
                    self.s.add(exp)
            for i in range(1,num+1):
                self.dicti["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(32)+',ctx=self.ctx)')
                self.dicti["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(32)+',ctx=self.ctx)')
                self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(32)+"))",self.dicti))
                self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)",self.dicti))
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"& _start____out_var_0_1(),ctx=local_ctx)",self.dicti))
            while (self.s.check() == sat and len(sols)<total):
                out=self.s.model()
                self.dicti['out']=out
                inputVal=[out[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long() for var in self.varNames]
                sols.append(inputVal)
                self.s.add(eval("_start____out_var_0_1()!=out[ _start____out_var_0_1]",self.dicti))
                expressions.append(eval(" _start____out_var_0_1()!=out[ _start____out_var_0_1]",self.dicti))
                #print(str(eval(" _start____out_var_0_1()!=out[ _start____out_var_0_1]",self.dicti)))
            self.s.pop()
            count+=1
        return sols


    def generateInput(self,num,total=20):
        inputVal=[]
        innerSols=[]
        self.s.push()
        self.dicti['local_ctx']=self.ctx
        for i in range(1,num+1):
            self.dicti["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(32)+',ctx=self.ctx)')
            self.dicti["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(32)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(32)+"))",self.dicti))
            self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)",self.dicti))
            self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"& _start____out_var_0_1(),ctx=local_ctx)",self.dicti))
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            self.dicti['out']=out
            try:
                inputVal=[out[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long() for var in self.varNames]
                outputVal=out[self.dicti['_start____out_var_0_1']].as_signed_long()
                innerSols.append((inputVal,outputVal))
                self.s.add(eval("_start____out_var_0_1()!=out[ _start____out_var_0_1]",self.dicti))
            except Exception:
                print("Empty out")
                print(self.varNames)
                print(out)
        self.s.pop()
        if(len(innerSols)>0):
            inputVal,outputVal=innerSols[random.randint(0,len(innerSols)-1)]
        else:
            inputVal=None
            outputVal=None
        return inputVal,outputVal

    def generateInputDiv(self,num,total=20):
        inputVal=[]
        innerSols=[]
        self.s.push()
        self.dicti['local_ctx']=self.ctx
        for i in range(1,num+1):
            self.dicti["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(32)+',ctx=self.ctx)')
            self.dicti["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(32)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(32)+"))",self.dicti))
            self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)",self.dicti))
            for var in self.varNames:
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"& _start__" + str(var) + "_0_1(),ctx=local_ctx)",self.dicti))
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            self.dicti['out']=out
            try:
                inputVal=[out[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long() for var in self.varNames]
                outputVal=out[self.dicti['_start____out_var_0_1']].as_signed_long()
                innerSols.append((inputVal,outputVal))
                express=['_start__'+str(var)+'_0_1()!=out[_start__'+str(var)+'_0_1]' for var in self.varNames]
                express="Or("+",".join(express)+")"
                self.s.add(eval(express,self.dicti))
            except Exception:
                print("Empty out")
                print(self.varNames)
                print(out)
        self.s.pop()
        if(len(innerSols)>0):
            inputVal,outputVal=innerSols[random.randint(0,len(innerSols)-1)]
        else:
            inputVal=None
            outputVal=None
        return inputVal,outputVal


    def generateInputDivParallel(self,num,total=20,worker):
        inputVal=[]
        innerSols=[]
        self.s.push()
        self.dicti['local_ctx']=self.ctx
        for i in range(1,num+1):
            self.dicti["instVar_a"+str(i)+"_" + str(worker)]=eval('BitVec("'+'instVar_a'+str(i)+"_" + str(worker)+'",'+str(32)+',ctx=self.ctx)')
            self.dicti["instVar_c"+str(i)+"_" + str(worker)]=eval('BitVec("'+'instVar_c'+str(i)+"_" + str(worker)+'",'+str(32)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"_" + str(worker)+"==randint(0,pow(2,"+str(32)+"))",self.dicti))
            self.s.add(eval("instVar_c"+str(i)+"_" + str(worker)+"==randint(0,1)",self.dicti))
            for var in self.varNames:
                self.s.add(eval("instVar_c"+str(i)+"_" + str(worker)+"==sub(instVar_a"+str(i)+"_" + str(worker)+"& _start__" + str(var) + "_0_1(),ctx=local_ctx)",self.dicti))
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            self.dicti['out']=out
            try:
                inputVal=[out[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long() for var in self.varNames]
                outputVal=out[self.dicti['_start____out_var_0_1']].as_signed_long()
                innerSols.append((inputVal,outputVal))
                express=['_start__'+str(var)+'_0_1()!=out[_start__'+str(var)+'_0_1]' for var in self.varNames]
                express="Or("+",".join(express)+")"
                self.s.add(eval(express,self.dicti))
            except Exception:
                print("Empty out")
                print(self.varNames)
                print(out)
        self.s.pop()
        if(len(innerSols)>0):
            inputVal,outputVal=innerSols[random.randint(0,len(innerSols)-1)]
        else:
            inputVal=None
            outputVal=None
        return inputVal,outputVal

    
    #This gets the output type
    def alignOutputs(self):
        ret=returnVisitor.ReturnVisitor()
        ret.visit(self.target)
        self.output=ret.getRetVal()
        ret.visit(self.target)
        outputAst=ret.getDecVal()
        self.outputType=outputAst.type.type.names[0]
