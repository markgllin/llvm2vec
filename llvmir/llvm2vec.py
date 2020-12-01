# https://github.com/McGill-DMaS/Kam1n0-Community/blob/2194aff10db8995d986ce92034a2fef70bca25f4/kam1n0/kam1n0-rep/src/main/java/ca/mcgill/sis/dmas/nlp/model/rsk/LearnerAsm2VecEmbdOnly.java
from numpy.lib.function_base import average
from .normalizer import Normalizer
import numpy as np
class LLVM2Vec:
  
  def average_vectors(vectors):
    num_of_vectors = len(vectors)

    data = np.array(vectors)
    return np.average(data, axis=0)

  joint_memory = average_vectors

  def concat_vectors(*vectors):
    return np.concatenate((vectors), axis=None)

  