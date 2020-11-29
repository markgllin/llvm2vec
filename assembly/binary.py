import llvmlite.binding as llvm
from .function import Function
from llvmir.vector import Vector

class Binary:

  def __init__(self, llvm_bytecode):
    self.functions =[]
    self.instr_freq_map = {}

    moduleref= llvm.parse_bitcode(llvm_bytecode)

    for func in moduleref.functions:
      llvm_func = Function(func)
      self.functions.append(llvm_func)

      for op in llvm_func.instr_freq_map:
        if op in self.instr_freq_map:
          self.instr_freq_map[op] += llvm_func.instr_freq_map[op]
        else:
          self.instr_freq_map[op] = llvm_func.instr_freq_map[op]
    
    self.total_tokens = sum(self.instr_freq_map.values())
    self.instr_vectors = self.generate_instr_vectors()
    self.func_vectors = self.get_func_vector_map()
    print(self.total_tokens)

  def generate_instr_vectors(self):
    instr_vectors = {}

    for op in self.instr_freq_map:
      instr_vectors[op] = Vector(op)

    return instr_vectors

  def get_func_vector_map(self):
    func_vectors = {}

    for func in self.functions:
      func_vectors[func.id] = func.vector

    return func_vectors