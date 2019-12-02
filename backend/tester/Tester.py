from pycparser import parse_file, c_generator
import cffi

class Tester:
    def __init__(self,fileName, functionName, inputs):
        self.fileName=fileName
        self.functionName=functionName
        self.inputs=inputs
        ast = parse_file(fileName)
        for func in ast.ext:
            if func.decl.name == functionName:
                self.ast=func


    def setAst(self,ast):
        self.ast=ast

    def testFunction(self):
        ffi=cffi.FFI()     
        generator = c_generator.CGenerator()
        #ffi.set_source(self.functionName,generator.visit(self.ast))
        ffi.cdef(generator.visit(self.ast.decl)+";")
        lib = ffi.verify(generator.visit(self.ast))
        #ffi.compile()
        #exec("import " + self.functionName)
        output=[]
        for inputVal in self.inputs:
            print("lib."+self.functionName+"("+','.join(str(x) for\
 x in inputVal)+")")
            output.append(eval("lib."+self.functionName+"("+','.join(str(x) for x in inputVal)+")"))
        return output

