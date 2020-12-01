# https://github.com/McGill-DMaS/Kam1n0-Community/blob/2194aff10db8995d986ce92034a2fef70bca25f4/kam1n0/kam1n0-rep/src/main/java/ca/mcgill/sis/dmas/nlp/model/astyle/NodeWord.java

import numpy as np

class Vector:

  def __init__(self, token, dimension):
    self.token = token
    self.dimension = dimension
    self.neuIn = self.neuIn()
    self.neuOut = self.neuOut()
  
  def neuIn(self):
    return np.random.uniform(low=0.01, high=0.5, size=self.dimension)

  def neuOut(self):
    return np.full(self.dimension, 0, dtype=float)