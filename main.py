from llvmir.function_cfg import FunctionCFG
from asm2vec.asm import Function
from asm2vec.model import Asm2Vec
import llvmlite.binding as llvm
import logging

logging.basicConfig(level=logging.DEBUG)

f = open("llvm_binary_example/app_rand.c.bc", "rb")
data=f.read()
f.close()

moduleref= llvm.parse_bitcode(data)

repo = []
for raw_func in moduleref.functions:
  cfg_func = FunctionCFG(raw_func)
  
  if cfg_func.blocks:
    repo.append(Function(cfg_func.root(), cfg_func.id))

model = Asm2Vec(d=200)
train_repo = model.make_function_repo(repo)
model.train(train_repo)