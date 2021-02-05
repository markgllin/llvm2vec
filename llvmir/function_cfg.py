import llvmlite.binding as llvm
import pygraphviz
import pydot
import re

from networkx.drawing import nx_agraph
from collections import defaultdict
from .normalizer import Normalizer
from asm2vec.asm import BasicBlock, parse_instruction
import pdb
class FunctionCFG:

  normalizer = Normalizer()

  def __init__(self, func, filename):
    self.blocks = defaultdict(lambda: BasicBlock())

    cfg = llvm.get_function_cfg(func, show_inst=True)
    self.graph = nx_agraph.from_agraph(pygraphviz.AGraph(cfg))

    (self.dot_graph,) = pydot.graph_from_dot_data(cfg)
    self.id = re.search("CFG for \'(.+?)\' function", self.dot_graph.get_label()).group(1) + '_' + filename
    self.generate_pngs()
    
    for block in self.graph.nodes(data = True):
      successors = self.get_block_successors(block[0])

      for successor in successors:
        # uses default dict val if self.blocks[block[0]] or self.blocks[successor] not initialized yet
        self.blocks[block[0]].add_successor(self.blocks[successor])

      for inst in self.normalize_block_contents(block):
        parsed_instruction = parse_instruction(inst)
        self.blocks[block[0]].add_instruction(parsed_instruction)

  def root(self):
    return self.blocks[next(iter(self.blocks))] if self.blocks else None

  def generate_pngs(self):
    self.dot_graph.write_png('cfgs/'+ self.id + '.png')

  def get_block_successors(self, block):
    # edge[0] = start node, edge[1] = destination node
    return [edge[1] for edge in self.graph.out_edges(block)]

  def normalize_block_contents(self, block):
    block_contents = []

    for line in block[1]["label"].split('\l'):
      line = line.strip()

      if line.startswith("..."):
        block_contents[-1] += line[3:]
      else:
        block_contents.append(line)

    # remove closing brace from list
    if block_contents[-1] == '}':
      del block_contents[-1]
    # remove conditional statements from list
    elif block_contents[-1][0] == '|':
      del block_contents[-1]

    # remove opening label from list
    if block_contents[0][-1] == ':':
      del block_contents[0]

    # remove opening label from list
    if block_contents[-1] == '}':
      del block_contents[-1]

    return self.normalizer.normalize(block_contents)

