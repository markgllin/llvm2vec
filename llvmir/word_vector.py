from .vector import Vector

class WordVector(Vector):
  def __init__(self, token, dimension=200):
    super().__init__(token, dimension)