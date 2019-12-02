from pycparser import parse_file, c_generator, c_ast

class TesterMain():
    def __init__(self,ast,functionName, inputs):
        self.functionName=functionName
        self.inputs=inputs
        self.ast=ast
        self.functype=ast.decl.type.type.type.names[0]
        self.funcs=[]
        self.varNames=list(param_decl.name for param_decl in self.ast.decl.type.args.params)
        self.varTypes=list(param_decl.type.type.names[0] for param_decl in self.ast.decl.type.args.params)

    def insertTest(self,block,functionName,varVals,varTypes):
        expressList = list(c_ast.Constant(type=varTypes[i],value=str(varVals[i])) for i in range(len(varVals)))
        funcCall = c_ast.FuncCall(c_ast.ID(name=functionName),c_ast.ExprList(expressList))
        block.body.block_items.insert(0,funcCall)

    def createMain(self):
        #Main Function
        #Declaration
        z1 = c_ast.TypeDecl('args',[],c_ast.IdentifierType(['int']))
        args = c_ast.Decl('args',[],[],[],z1,None,None)
        z2= c_ast.PtrDecl([],c_ast.TypeDecl('argv',[],c_ast.IdentifierType(['char'])))
        z3=c_ast.ArrayDecl(z2,None,[])
        argv = c_ast.Decl('argv',[],[],[],z3,None,None)
        params=c_ast.ParamList([args,argv])
        mainDec=c_ast.FuncDecl(params,c_ast.TypeDecl('main',[],c_ast.IdentifierType(['int'])))
#        insertTest(functionName,varVals,varTypes)
        #Body
        returnStmt=c_ast.Return(c_ast.Constant(type="int",value="0"))
        comp=c_ast.Compound([returnStmt])
        return c_ast.FuncDef(mainDec,None,comp)

    def createProgram(self):
        self.prog=c_ast.FileAST([self.ast,self.main])

    def dumpTests(self,fileName="output.c"):
        self.main =  self.createMain()
        generator = c_generator.CGenerator()
        for inputVal in self.inputs:
            self.insertTest(self.main,self.functionName,inputVal,self.varTypes)
        self.createProgram()
        f=open(fileName,"w")
        f.write(generator.visit(self.prog))
        f.close()

    
