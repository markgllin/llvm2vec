import llvmlite.binding as llvm
from asm2vec.asm import Function
from .function_cfg import FunctionCFG
import os
from os import listdir
from os.path import isfile, join, basename


class IRReader:

  def __init__(self):
    self

  def process_directory(self, dir):
    files = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.bc')]
    
    functions = []
    for file in files:
      functions += self.parse_bc_file(file)
    
    return functions

  def parse_bc_file(self, file):
    filename=basename(file)

    print("Reading file: " + str(file))
    f = open(file, "rb")
    data = f.read()
    f.close()

    print("Parsing bc...")
    moduleref = llvm.parse_bitcode(data)

    functions = []
    for raw_func in moduleref.functions:
      cfg_func = FunctionCFG(raw_func, filename)
      
      if cfg_func.blocks:
        functions.append(Function(cfg_func.root(), name = cfg_func.id, filename = filename))
    
    return functions