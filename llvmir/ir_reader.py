import llvmlite.binding as llvm
from asm2vec.asm import Function
from .function_cfg import FunctionCFG

class IRReader:

  def __init__(self):
    self

  def parse_bc_file(self, file):
    print("Reading file: " + str(file))
    f = open(file, "rb")
    data = f.read()
    f.close()

    print("Parsing bc...")
    moduleref = llvm.parse_bitcode(data)

    functions = []
    for raw_func in moduleref.functions:
      cfg_func = FunctionCFG(raw_func)
      
      if cfg_func.blocks:
        functions.append(Function(cfg_func.root(), cfg_func.id))
    
    return functions