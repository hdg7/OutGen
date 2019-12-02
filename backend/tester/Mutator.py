from pycparser import parse_file, c_generator, c_ast
import copy
import random

class Mutator:

    lOAAN=["+","-","/","%","*"]
    lOPPO=["p++","p--","++","--"]
    
    def __init__(self,fileName,functionName,probability=0.5):
        self.ast = parse_file(fileName)
        self.probability=probability
        for idx,func in enumerate(self.ast.ext):
            if func.decl.name == functionName:
                self.target=func
                self.index=idx

    def isOAAN(self,operator):
        return operator in self.lOAAN
    def isOPPO(self,operator):
        return operator in self.lOPPO

    def changeOp(self,listOps,operator=""):
        if operator in listOps:
            listOps.remove(operator)
        return listOps[random.randint(0,len(listOps)-1)]
    
    def changeOAAN(self,operator=""):
        l=copy.copy(self.lOAAN)
        return self.changeOp(l,operator)

    
    def changeOPPO(self,operator=""):
        l=copy.copy(self.lOPPO)
        return self.changeOp(l,operator)
    
    def visit_ast(self,ast):
        if isinstance(ast, tuple):
            ast = ast[1]
            return self.visit_ast(ast)
        for attr in ast.attr_names:
            if(self.isOAAN(getattr(ast,attr)) and random.random() < self.probability):
                setattr(ast,attr,self.changeOAAN(getattr(ast,attr)))
            if(self.isOPPO(getattr(ast,attr)) and random.random() < self.probability):
                setattr(ast,attr,self.changeOPPO(getattr(ast,attr)))
        for c in ast.children():
            self.visit_ast(c)

    def getNames(self):
        return self.programNames

    def getMutants(self):
        return self.mutant
    
    def mutate(self,numMutants):
        self.mutant=[]
        for i in range(numMutants):
            self.mutant.append(copy.deepcopy(self.target))
            self.visit_ast(self.mutant[i])
            
