from llvmir.vector import Vector

class WordVector():

  def __init__(self, token, dimension):
    self.neu = Vector(token, dimension)
    self.neu_prime = Vector(token, dimension, False)