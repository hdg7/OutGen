from pycparser import parse_file
from random import randint
from z3 import *
from ..support.functions import sub
from ..visitors.cVisitors.ReturnVisitor import ReturnVisitor
from ..visitors.cVisitors.LocalVisitor import LocalVisitor
from .InputGenerator import InputGenerator
import random
import copy

class ConstraintInputGenerator(InputGenerator):

    def __init__(self,fileName,functionName):
        InputGenerator.__init__(self,fileName,functionName)
        visitor = LocalVisitor()
        self.varLocals = visitor.getVariables(self.target)
    
    def setConstraints(self,solver,guardNum):
        self.ctx=Context()
        self.s=solver.translate(self.ctx)
        self.guardNum=guardNum
        self.retry=10
    def generateInputs(self,total,num,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        count=0
        sols=[]
        expressions=[]
        while((count< self.retry) and (len(sols)<total)):
            self.s.push()
            if(len(expressions)>0):
                for exp in expressions:
                    self.s.add(eval(exp))
            for i in range(1,num+1):
                globals()["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(l)+',ctx=self.ctx)')
                globals()["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(l)+',ctx=self.ctx)')
                self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(l)+"))"))
                self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)"))
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"&retVal,ctx=self.ctx)"))
            while (self.s.check() == sat and len(sols)<total):
                out=self.s.model()
                sols.append(out)
                self.s.add(retVal!=out[retVal])
                expressions.append(str(retVal!=out[retVal]))
                print(str(retVal!=out[retVal]))
            self.s.pop()
            count+=1
        return sols

    def generateWithInputs(self,total,num,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        guardVec=BitVec('guardVec',self.guardNum,ctx=self.ctx)
        count=0
        sols=[]
        expressions=[]
        while((count< self.retry) and (len(sols)<total)):
            self.s.push()
            if(len(expressions)>0):
                for exp in expressions:
                    self.s.add(eval(exp))
            for i in range(1,num+1):
                globals()["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(l)+',ctx=self.ctx)')
                globals()["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(l)+',ctx=self.ctx)')
                self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(l)+"))"))
                self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)"))
                self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"&retVal,ctx=self.ctx)"))
            while (self.s.check() == sat and len(sols)<total):
                out=self.s.model()
                sols.append(out)
                self.s.add(Or(retVal!=out[retVal],guardVec!=out[guardVec],self.ctx))
                expressions.append(str(Or(retVal!=out[retVal],guardVec!=out[guardVec],self.ctx)))
            self.s.pop()
            count+=1
        return sols

    def generateOutputLimited(self,num,sols,total,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        for i in range(1,num+1):
            globals()["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            globals()["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(l)+"))"))
            self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)"))
            self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"&retVal,ctx=self.ctx)"))
        innerSols=[]
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            innerSols.append(out)
            self.s.add(retVal!=out[retVal])
        if(len(innerSols)>0):
            out=innerSols[random.randint(0,len(innerSols)-1)]
            sols.append(out[retVal])


    def generateOutput(self,num,sols,total,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        for i in range(1,num+1):
            globals()["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            globals()["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(l)+"))"))
            self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)"))
            self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"&retVal,ctx=self.ctx)"))
        innerSols=[]
        while (self.s.check() == sat):
            out=self.s.model()
            innerSols.append(out)
            self.s.add(retVal!=out[retVal])
        if(len(innerSols)>0):
            out=innerSols[random.randint(0,len(innerSols)-1)]
            sols.append(out[retVal])

    def generateOutputParallel(self,num,sols,locker,worker,total,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        dicti={"retVal":retVal,"self":self}
        print(worker)
        for i in range(1,num+1):
            dicti["instVar_a"+str(i)+"_" + str(worker)]=eval('BitVec("'+'instVar_a'+str(i)+"_" + str(worker)+'",'+str(l)+',ctx=self.ctx)')
            dicti["instVar_c"+str(i)+"_" + str(worker)]=eval('BitVec("'+'instVar_c'+str(i)+"_" + str(worker)+'",'+str(l)+',ctx=self.ctx)')
#            print("a"+str(i)+"_" + str(worker)+"==randint(0,pow(2,"+str(l)+"))")
            dicti.update(globals())
            self.s.add(eval("instVar_a"+str(i)+"_" + str(worker)+"==randint(0,pow(2,"+str(l)+"))",dicti))
            self.s.add(eval("instVar_c"+str(i)+"_" + str(worker)+"==randint(0,1)",dicti))
            self.s.add(eval("instVar_c"+str(i)+"_" + str(worker)+"==sub(instVar_a"+str(i)+"_" + str(worker)+"&retVal,self.ctx)",dicti))
        innerSols=[]
        #print(dicti)
        while (self.s.check() == sat):
            out=self.s.model()
            innerSols.append(out)
            self.s.add(retVal!=out[retVal])
        if(len(innerSols)>0):
            out=innerSols[random.randint(0,len(innerSols)-1)]
            with locker:
                sols.append(out[retVal])
            
    def generateOutputExtra(self,num,sols,total,l=16):
        self.l=l
        retVal=BitVec('retVal',l,ctx=self.ctx)
        for i in range(1,num+1):
            globals()["instVar_a"+str(i)]=eval('BitVec("'+'instVar_a'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            globals()["instVar_c"+str(i)]=eval('BitVec("'+'instVar_c'+str(i)+'",'+str(l)+',ctx=self.ctx)')
            self.s.add(eval("instVar_a"+str(i)+"==randint(0,pow(2,"+str(l)+"))"))
            self.s.add(eval("instVar_c"+str(i)+"==randint(0,1)"))
            self.s.add(eval("instVar_c"+str(i)+"==sub(instVar_a"+str(i)+"&retVal,ctx=self.ctx)"))
        innerSols=[]
        while (self.s.check() == sat and len(innerSols)<total):
            out=self.s.model()
            innerSols.append(out)
            self.s.add(retVal!=out[retVal])
        if(len(innerSols)>0):
            out=innerSols[random.randint(0,len(innerSols)-1)]
            sols.append(out)
        
    
    def alignOutputs(self):
        ret=returnVisitor.ReturnVisitor()
        ret.visit(self.target)
        self.output=ret.getRetVal()
        ret.visit(self.target)
        outputAst=ret.getDecVal()
        self.outputType=outputAst.type.type.names[0]

    def addConstraintInputs(self,sol,solver):
        inputContraint=[]
        finalExp=[]
        for inName in self.varNames:
            inputContraint.append(min(list(filter(lambda x:inName in x, [str(y) for y in sol.decls()])),key=len))
        for i in inputContraint:
            globals()[i]=eval('BitVec("'+i+'",'+str(self.l)+',ctx=self.ctx)')
            finalExp.append(i + " != " + str(sol[eval(i)]))
        final="Or("+",".join(finalExp)+")"
        solver.add(final)
        return finalInputs

    def findValuesNames(self):
        if(self.s.check()== unsat):
            return
        sol=self.s.model()
        self.varConstraints=[]
        for inName in (self.varLocals+self.varNames):
            values=list(filter(lambda x:inName+"_" in x, [str(y) for y in sol.decls()]))
            print(values)
            finalLen=len(max(values,key=len))
            print(finalLen)
            potentValues=list([value for value in values if len(value)==finalLen])
            print(potentValues)
            self.varConstraints.append(max(potentValues))      
        return self.varConstraints
        
        
    def findInputsValues(self,sols):
        self.inputContraint=[]
        self.finalInputs=[]
        for inName in self.varNames:
            self.inputContraint.append(min(list(filter(lambda x:inName+"_" in x,[elem for elem in [str(y) for y in sols[0].decls()] if not elem.startswith('instVar')])),key=len))
        for i in self.inputContraint:
            globals()[i]=eval('BitVec("'+i+'",'+str(self.l)+',ctx=self.ctx)')
        for sol in sols:
            self.finalInputs.append(list(sol[eval(elem)].as_signed_long() for elem in self.inputContraint))
        return self.finalInputs

    def findLocalsValues(self,sols):
        self.localContraint=[]
        self.finalLocals=[]
        for inName in (self.varLocals+self.varNames):
            self.localContraint.append(max(list(filter(lambda x:inName+"_" in x,[elem for elem in [str(y) for y in sols[0].decls()] if not elem.startswith('instVar')])),key=len))
        for i in self.localContraint:
            globals()[i]=eval('BitVec("'+i+'",'+str(self.l)+',ctx=self.ctx)')
        for sol in sols:
            self.finalLocals.append(list(sol[eval(elem)].as_signed_long() for elem in self.localContraint))
        return self.finalLocals
