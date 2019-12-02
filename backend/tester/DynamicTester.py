from pycparser import parse_file, c_generator
import cffi

class DynamicTester:
    def __init__(self,fileName, functionName):
        self.fileName=fileName
        self.loaded=False
        self.functionName=functionName
        ast = parse_file(fileName)
        for func in ast.ext:
            if func.decl.name == functionName:
                self.ast=func
    def updateAst(self,ast):
        self.ast=ast
    def loadTester(self):
        self.ffi=cffi.FFI()
        generator = c_generator.CGenerator()
        self.ffi.cdef(generator.visit(self.ast.decl)+";")
        self.lib = self.ffi.verify(generator.visit(self.ast))
        self.loaded=True
    def testFunction(self,inputs):
        if not(self.loaded):
            self.loadTester()
        output=[]
        for inputVal in inputs:
            output.append(eval("self.lib."+self.functionName+"("+','.join(str(x) for x in inputVal)+")"))
        return output

