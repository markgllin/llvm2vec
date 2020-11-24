
import llvmlite.binding as llvm
from llvmir.llvm2vec import LLVM2Vec
from assembly.function import Function

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

f = open("llvm_binary_example/hello.bc", "rb")
data=f.read()
f.close()
llvm_ir = data
moduleref= llvm.parse_bitcode(llvm_ir)
functions = moduleref.functions

# LLVM2Vec.process(functions)

llvm_functions = []

for func in functions:
  llvm_functions.append(Function(func))

# LLVM2Vec.generate_frequency_map(llvm_functions)
  # asm_functions.append(llvm_function)


  