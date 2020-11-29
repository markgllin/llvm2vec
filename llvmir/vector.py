# https://github.com/McGill-DMaS/Kam1n0-Community/blob/2194aff10db8995d986ce92034a2fef70bca25f4/kam1n0/kam1n0-rep/src/main/java/ca/mcgill/sis/dmas/nlp/model/astyle/NodeWord.java

from numpy import random as rand

class Vector:

  DIMENSION = 100

  def __init__(self, token):
    self.token = token
    self.neuIn = self.neuIn()
    self.neuOut = self.neuOut()
  
  def neuIn(self):
    return rand.uniform(low=0.01, high=0.5, size=self.DIMENSION)

  def neuOut(self):
    return [0] * self.DIMENSION