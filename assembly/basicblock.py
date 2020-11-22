import llvmlite.binding as llvm
from networkx.drawing import nx_agraph
import pygraphviz
class Block:

  def __init__(self, block, edges):
    self.block = block
    self.block_name = self.block[0]
    self.edges = edges

    self.block_contents = []
    for line in self.block[1]["label"].split('\l'):
      line = line.strip()

      if line.startswith("..."):
        self.block_contents[-1] += line[3:]
      else:
        self.block_contents.append(line)


    # remove closing brace from list
    if self.block_contents[-1] == '}':
      del self.block_contents[-1]
    # remove conditional statements from list
    elif self.block_contents[-1][0] == '|':
      del self.block_contents[-1]

    # remove opening label from list
    if self.block_contents[0][-1] == ':':
      del self.block_contents[0]

    # remove opening label from list
    if self.block_contents[-1] == '}':
      del self.block_contents[-1]