
import llvmlite.binding as llvm

from assembly.function import Function
from llvmir.normalizer import Normalizer

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

f = open("llvm_binary_example/hello.bc", "rb")
data=f.read()
f.close()
llvm_ir = data
moduleref= llvm.parse_bitcode(llvm_ir)
functions = moduleref.functions

asm_functions = []
for func in functions:
  llvm_function = Function(func)
  asm_functions.append(llvm_function)

  traces = llvm_function.generate_execution_traces()
  llvm_parser = Normalizer()
  for trace in traces:
    normalized = llvm_parser.normalize(trace)
    print(normalized)



  