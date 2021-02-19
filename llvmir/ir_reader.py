import llvmlite.binding as llvm
from asm2vec.asm import Function
from .function_cfg import FunctionCFG
from .function_inliner import get_cfg, get_cfg_map, get_in_degree_from_map
import os
from os import listdir
from os.path import isfile, join, basename

class IRReader:

  def __init__(self):
    self

  def process_directory(self, dir, opt = ""):
    files = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f)) and f.endswith('.bc')]
    
    functions = {}
    for file in files:
      functions = {**functions, **self.parse_bc_file(file, opt)}
    
    return functions

  def parse_bc_file(self, file, opt):
    cfg_path = "cfgs/" + opt + "/"

    if not os.path.exists(cfg_path):
      os.makedirs(cfg_path)

    print("\tParsing bc...")
    data = self.read_bc_file(file)
    moduleref = llvm.parse_bitcode(data)

    function_map = {}
    file_id= "[" + basename(file) + "]"

    cfg_map = get_cfg_map(moduleref.functions)
    cfg_map = get_in_degree_from_map(cfg_map)

    for function in cfg_map:
      cfg_func = FunctionCFG(function, cfg_map)
      cfg_func.generate_pngs(cfg_path)

      if cfg_func._blocks:
        asm_function = Function(cfg_func.root(), name = cfg_func._name)
        function_map[cfg_func._name + file_id] = {'asm_function': asm_function, 'cfg': cfg_func, 'filename': file_id}
    
    return function_map


  def read_bc_file(self, file):
    print("Reading file: " + str(file))
    f = open(file, "rb")
    data = f.read()
    f.close()

    return data