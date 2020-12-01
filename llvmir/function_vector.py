from .vector import Vector

class FunctionVector(Vector):
  def __init__(self, token, dimension=200):
    super().__init__(token, 2*dimension)