from z3 import *
from .InputGenerator import InputGenerator
from random import randint

class BasicSolverGenerator(InputGenerator):
    
    def __init__(self,fileName,functionName,filez3):
        InputGenerator.__init__(self,fileName,functionName)
        self.ctx = Context()
        self.f = parse_smt2_file(filez3,ctx=self.ctx)
        print(self.f)
        self.dicti={}
        for pos,var in enumerate(self.varNames):
            if self.varTypes[pos]=="int" or self.varTypes[pos]=="bool":
                self.dicti["_start__"+str(var)+"_0_1"]=eval('Function("'+'_start__'+str(var)+'_0_1",BitVecSort(32,self.ctx))')
                print("_start__"+str(var)+"_0_1")
            elif self.varTypes[pos]=="float" or  self.varTypes[pos]=="double":
                self.dicti["_start__"+str(var)+"_0_1"]=eval('Function("'+'_start__'+str(var)+'_0_1",FloatDouble(self.ctx))')
        self.dicti.update(globals())

    def stats(self):
        print("Vars:" + str(len(self.varNames)))
        
    def createSolver(self):
        self.solver=Solver(ctx=self.ctx)
        self.solver.add(self.f)

    def finalSetUp(self):
        self.createSolver()

    def createInput(self):
        solCheck=self.solver.check()
        if(str(solCheck)=='sat'):
            sol=self.solver.model()
            input=[sol[self.dicti['_start__'+str(var)+'_0_1']].as_signed_long() for var in self.varNames]
            return(input)


    def createDifInputs(self,total):
        self.solver.push()
        inputs=[]
        for i in range(total):
            solCheck=self.solver.check()
            if(str(solCheck)=='sat'):
                sol=self.solver.model()
                self.dicti['sol']=sol
                print(sol)
                print(self.varNames)
                print(self.varTypes)
                inputVal=[]
                for pos,var in enumerate(self.varNames):
                    if self.varTypes[pos]=="int" or self.varTypes[pos]=="bool":
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
                            print(var)
                            print('_start__'+str(var)+'_0_1')
                            print(self.dicti['_start__'+str(var)+'_0_1'])
                            print(sol[self.dicti['_start__'+str(var)+'_0_1']])
                            inputVal.append(eval(str(sol[self.dicti['_start__'+str(var)+'_0_1']])))
                chosenIn=randint(0,len(self.varNames)-1)
                #print(self.dicti)
                if not(str(sol[self.dicti['_start__'+str(self.varNames[chosenIn])+'_0_1']]) in ["NaN","oo","+oo","-oo"]):
                    print("Var: ",str(sol[self.dicti['_start__'+str(self.varNames[chosenIn])+'_0_1']]))
                    print("Input: ",inputVal)
                    self.solver.add(eval('_start__'+str(self.varNames[chosenIn])+'_0_1() != ' + str(sol[self.dicti['_start__'+str(self.varNames[chosenIn])+'_0_1']]),self.dicti))
                inputs.append(inputVal)
        self.solver.pop()
        return(inputs)

            
