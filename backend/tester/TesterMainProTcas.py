from pycparser import parse_file, c_generator, c_ast
from .TesterMain import TesterMain
class TesterMainPro(TesterMain):

    def insertTest(self,block,functionName,varVals,varTypes,timer):
        #Fork call
        cFork=c_ast.Assignment( lvalue=c_ast.ID(name='child_pid'), op='=', rvalue=c_ast.FuncCall( c_ast.ID(name='fork'), args=None))
        #Child
        if self.functype=='int' or self.functype=="bool":
            printLeft=c_ast.Constant(type="char",value='"'+"%d" +'"')
        elif self.functype=='float' or self.functype=='double':
            printLeft=c_ast.Constant(type="char",value='"'+"%f" +'"')
        else:
            printLeft=c_ast.Constant(type="char",value='"'+"%d" +'"')
        
        expressList = list(c_ast.Constant(type=varTypes[i],value=str(varVals[i])) for i in range(len(varVals)))
        funcCall = c_ast.FuncCall(c_ast.ID(name=functionName),c_ast.ExprList(expressList))
        expressList = [printLeft,funcCall]        
        funcCall = c_ast.FuncCall(c_ast.ID(name="printf"),c_ast.ExprList(expressList))
        
        funcCall2 = c_ast.FuncCall(c_ast.ID(name="exit"),c_ast.ExprList([c_ast.Constant(type='int',value='0')]))
        #Parent
        cAlarm=c_ast.FuncCall( c_ast.ID(name='alarm'),c_ast.ExprList([c_ast.Constant(type='int',value=str(timer))]))
        cWait=c_ast.FuncCall( c_ast.ID(name='wait'),c_ast.ExprList([c_ast.ID(name='0')]))
        #IFs
        if_false= c_ast.If( c_ast.BinaryOp(left=c_ast.ID(name='child_pid'),op='==',right= c_ast.Constant(type='int',value='0')), c_ast.Compound([funcCall,funcCall2]),iffalse=None)
        if_ini=c_ast.If( c_ast.BinaryOp(left=c_ast.ID(name='child_pid'),op='>',right= c_ast.Constant(type='int',value='0')), c_ast.Compound([cAlarm,cWait]),iffalse=if_false)
        block.body.block_items.insert(1,if_ini)
        block.body.block_items.insert(1,cFork)

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
        ##Signal
        sigalrm=c_ast.ID(name="14")
        funcCast=c_ast.TypeDecl(declname = None,quals=[],type=c_ast.IdentifierType(['void']))
        paramCast=c_ast.ParamList([c_ast.Typename(name=None,quals=[],type=c_ast.TypeDecl(declname = None,quals=[],type=c_ast.IdentifierType(['int'])))])
        typeFunc=c_ast.PtrDecl(type=c_ast.FuncDecl(paramCast,funcCast),quals=[])        
        kchild=c_ast.Cast(to_type=c_ast.Typename(name=None, quals=[],type=typeFunc),expr=c_ast.ID(name="kill_child"))
        expressList = [sigalrm,kchild]
        signalStmt=c_ast.FuncCall(c_ast.ID(name="signal"),c_ast.ExprList(expressList))

        ##Return
        returnStmt=c_ast.Return(c_ast.Constant(type="int",value="0"))
        comp=c_ast.Compound([signalStmt,returnStmt])
        return c_ast.FuncDef(mainDec,None,comp)

    def createProgram(self):
        self.prog=c_ast.FileAST([self.ast,self.main])

    def addOtherFuncs(self,functions):
        self.funcs=functions
                        
    def dumpTests(self,fileName="output.c"):
        self.main =  self.createMain()
        generator = c_generator.CGenerator()
        for inputVal in self.inputs:
            self.insertTest(self.main,self.functionName,inputVal,self.varTypes,4)
        self.createProgram()
        f=open(fileName,"w")
        for func in self.funcs:
            #print(generator.visit(func))
            f.write(generator.visit(func))
            if not(isinstance(func,c_ast.FuncDef)):
                f.write(";\n")
        f.write(generator.visit(self.prog))
        f.close()

    
