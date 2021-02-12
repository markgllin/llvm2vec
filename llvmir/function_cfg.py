import llvmlite.binding as llvm
import pygraphviz
import pydot
import re

from networkx.drawing import nx_agraph
from collections import defaultdict
from .normalizer import Normalizer
from asm2vec.asm import BasicBlock, parse_instruction

class FunctionCFG:
  IDENTIFIERS = "[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*"
  normalizer = Normalizer()

  def __init__(self, func):
    cfg = llvm.get_function_cfg(func, show_inst=True)

    self._identifiers = []
    self._blocks = defaultdict(lambda: BasicBlock())
    self._graph = self.get_function_graph(cfg)
    self._dot_graph = self.get_dot_graph(cfg)
    self._name = self.get_function_name()
    
    for block in self._graph.nodes(data = True):
      successors = self.get_block_successors(block[0])

      for successor in successors:
        # uses default dict val if self.blocks[block[0]] or self.blocks[successor] not initialized yet
        self._blocks[block[0]].add_successor(self._blocks[successor])

      stripped_block = self.strip_block(block)
      self._identifiers += self.get_block_identifiers(stripped_block)
      normalized_contents = self.normalizer.normalize(stripped_block)

      # print(normalized_contents)
      # print(self._identifiers)

      for inst in normalized_contents:
        parsed_instruction = parse_instruction(inst)
        self._blocks[block[0]].add_instruction(parsed_instruction)

  def root(self):
    return self._blocks[next(iter(self._blocks))] if self._blocks else None

  def generate_pngs(self, filepath):
    print("\tGenerating cfg for " + self._name)
    self._dot_graph.write_png(filepath + self._name + '.png')

  def get_block_successors(self, block):
    # edge[0] = start node, edge[1] = destination node
    return [edge[1] for edge in self._graph.out_edges(block)]

  def get_function_name(self):
    return re.search("CFG for \'(.+?)\' function", self._dot_graph.get_label()).group(1)

  def get_function_graph(self, cfg):
    return nx_agraph.from_agraph(pygraphviz.AGraph(cfg))

  def get_dot_graph(self, cfg):
    (graph,) = pydot.graph_from_dot_data(cfg)
    return graph

  def get_block_identifiers(self, block):
    identifiers = []

    for inst in block:
      identifier = re.search(self.IDENTIFIERS, inst)
      if identifier:
        identifiers.append(identifier.group(0)[1:])

    return identifiers

  def strip_block(self, block):
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

    return block_contents