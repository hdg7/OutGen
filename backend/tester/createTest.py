from pycparser import parse_file, c_generator, c_ast

#Returns a function call at the beginning of the function
def insertTest(block,functionName,varVals,varTypes):
   expressList = list(c_ast.Constant(type=varTypes[i],value=varVals[i]) for i in range(len(varVals)))
   funcCall = c_ast.FuncCall(c_ast.ID(name=functionName),c_ast.ExprList(expressList))
   block.body.block_items.insert(0,funcCall)

def createTest(block,functionName,varVals,varTypes):
   #Main Function
   #Declaration
   z1 = c_ast.TypeDecl('args',[],c_ast.IdentifierType(['int']))
   args = c_ast.Decl('args',[],[],[],z1,None,None)
   z2= c_ast.PtrDecl([],c_ast.TypeDecl('argv',[],c_ast.IdentifierType(['char'])))
   z3=c_ast.ArrayDecl(z2,None,[])
   argv = c_ast.Decl('argv',[],[],[],z3,None,None)
   params=c_ast.ParamList([args,argv])
   mainDec=c_ast.FuncDecl(params,c_ast.TypeDecl('main',[],c_ast.IdentifierType(['int'])))
   insertTest(functionName,varVals,varTypes)
   #Body
   returnStmt=c_ast.Return(c_ast.Constant(type="int",value="0"))
   comp=c_ast.Compound([returnStmt])
   main= c_ast.FuncDef(mainDec,None,comp)
   insertTest(main,"func",['1','2'],['int','int'])
