
import llvmlite.binding as llvm

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

asm_functions = []
for func in functions:


  asm_functions.append(Function(func))
  # for u, v, keys, weight in graph.edges(data="weight", keys=True):
  #   print(weight)
  # print(type(graph).__name__)
  # blocks = function.blocks
  # for block in blocks:
  #   insts = block.instructions
  #   for inst in insts:
  #     print()d
  #     print("========")
  #     print("inst:" + str(inst))
  #     print("opcode:" + str(inst.opcode))
  #     print()
  #     operands = inst.operands
  #     for operand in operands:
  #       print("operand:" + str(operand))
  #       print("also inst:" + str(operand.is_instruction))
  #       attrs = operand.attributes
  #       for attr in attrs:
  #         print("\tattr:" + str(attr))