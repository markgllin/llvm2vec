# https://github.com/McGill-DMaS/Kam1n0-Community/blob/2194aff10db8995d986ce92034a2fef70bca25f4/kam1n0/kam1n0-rep/src/main/java/ca/mcgill/sis/dmas/nlp/model/rsk/LearnerAsm2VecEmbdOnly.java
from .normalizer import Normalizer
from assembly.function import Function

class LLVM2Vec:

  def generate_frequency_map(functions):
    frequency_map = {}
    
    for func in functions:
      for block_name in func.blocks:
        block = func.blocks[block_name]

        print(block.block_contents)