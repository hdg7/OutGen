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
        self.outTypeIndex=self.varNames.index('__out_var')
        self.varNames.remove('__out_var')
        for pos,var in  enumerate(self.varNames):
            if self.varTypes[pos]=="int":            
                self.dicti["_start__"+str(var)+"_0_1"]=eval('Function("'+'_start__'+str(var)+'_0_1",BitVecSort(32,self.ctx))')
            elif self.varTypes[pos]=="float" or  self.varTypes[pos]=="double":
                self.dicti["_start__"+str(var)+"_0_1"]=eval('Function("'+'_start__'+str(var)+'_0_1",FloatDouble(self.ctx))')
        if self.varTypes[self.outTypeIndex]=="int":
            self.dicti["_start____out_var_0_1"]=eval('Function("_start____out_var_0_1",BitVecSort(32,self.ctx))')
        elif self.varTypes[self.outTypeIndex]=="float" or  self.varTypes[self.outTypeIndex]=="double":
            self.dicti["_start____out_var_0_1"]=eval('Function("_start____out_var_0_1",FloatDouble(self.ctx))')
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
                print(out)
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
            if self.varTypes[self.outTypeIndex]=="int":
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"& _start____out_var_0_1(),ctx=local_ctx)",self.dicti))
            elif self.varTypes[self.outTypeIndex] in ["float","double"]:
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"& fpToUBV(RTZ(), _start____out_var_0_1() , BitVecSort(32,ctx=local_ctx),ctx=local_ctx),ctx=local_ctx)",self.dicti))
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            print(out)
            print(len(innerSols))
            self.dicti['out']=out
            #            try:
            inputVal=[]
            for pos,var in enumerate(self.varNames):
                print(self.varTypes[pos])
                print(var)
                if self.varTypes[pos]=="int":
                    inputVal.append(out[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long())
                elif self.varTypes[pos]=="float" or self.varTypes[pos]=="double":
                    if str(out[self.dicti['_start__'+str(var)+'_0_1']])=="oo":
                        inputVal.append('INFINITY')
                    elif str(out[self.dicti['_start__'+str(var)+'_0_1']])=="+oo":
                        inputVal.append('INFINITY')
                    elif str(out[self.dicti['_start__'+str(var)+'_0_1']])=="-oo":
                        inputVal.append('-INFINITY')
                    elif str(out[self.dicti['_start__'+str(var)+'_0_1']])=="NaN":
                        inputVal.append('void')
                    else:
                        inputVal.append(eval(str(out[self.dicti['_start__'+str(var)+'_0_1']])))
            if self.varTypes[self.outTypeIndex]=="int":
                outputVal=out[self.dicti['_start____out_var_0_1']].as_signed_long()
            elif self.varTypes[self.outTypeIndex]=="float" or self.varTypes[self.outTypeIndex]=="double":
                if str(out[self.dicti['_start____out_var_0_1']])=="oo":
                    outputVal='INFINITY'
                elif str(out[self.dicti['_start____out_var_0_1']])=="+oo":
                    outputVal='INFINITY'
                elif str(out[self.dicti['_start____out_var_0_1']])=="-oo":
                    outputVal='-INFINITY'
                elif str(out[self.dicti['_start____out_var_0_1']])=="NaN":
                    outputVal='void'
                else:
                    outputVal=eval(str(out[self.dicti['_start____out_var_0_1']]))
            else:
                print("Error")
                print(self.varTypes[self.outTypeIndex])
                print(str(out[self.dicti['_start____out_var_0_1']]))
                outputVal=None
            innerSols.append((inputVal,outputVal))
            self.s.add(eval("_start____out_var_0_1()!=out[ _start____out_var_0_1]",self.dicti))
#            except Exception:
#                print("Empty out")
#                print(self.varNames)
#                print(out)
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
            sol=self.s.model()
            print("Generated Out:")
            print(sol)
            self.dicti['sol']=sol
            inputVal=[]
            for pos,var in enumerate(self.varNames):
                if self.varTypes[pos]=="int":
                    inputVal.append(sol[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long())
                elif self.varTypes[pos]=="float" or self.varTypes[pos]=="double":
                    if str(sol[self.dicti['_start__'+str(var)+'_0_1']])=="oo":
                        inputVal.append('INFINITY')
                    elif str(sol[self.dicti['_start__'+str(var)+'_0_1']])=="+oo":
                        inputVal.append('INFINITY')
                    elif str(sol[self.dicti['_start__'+str(var)+'_0_1']])=="-oo":
                        inputVal.append('-INFINITY')
                    elif str(sol[self.dicti['_start__'+str(var)+'_0_1']])=="NaN":
                        inputVal.append('void')
                    else:
                        inputVal.append(eval(str(sol[self.dicti['_start__'+str(var)+'_0_1']])))
            if self.varTypes[self.outTypeIndex]=="int":
                outputVal=sol[self.dicti['_start____out_var_0_1']].as_signed_long()
            elif self.varTypes[pos]=="float" or self.varTypes[pos]=="double":
                if str(sol[self.dicti['_start____out_var_0_1']])=="oo":
                    outputVal='INFINITY'
                elif str(sol[self.dicti['_start____out_var_0_1']])=="+oo":
                    outputVal='INFINITY'
                elif str(sol[self.dicti['_start____out_var_0_1']])=="-oo":
                    outputVal='-INFINITY'
                elif str(sol[self.dicti['_start____out_var_0_1']])=="NaN":
                    outputVal='void'
                else:
                    outputVal=eval(str(sol[self.dicti['_start__'+str(var)+'_0_1']]))
            innerSols.append((inputVal,outputVal))
#                express=['_start__'+str(var)+'_0_1()!=out[_start__'+str(var)+'_0_1]' for var in self.varNames]
#                express="Or("+",".join(express)+")"
#                self.s.add(eval(express,self.dicti))
            #print("Empty out")
            #print(self.varNames)
            #print(sol)
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
