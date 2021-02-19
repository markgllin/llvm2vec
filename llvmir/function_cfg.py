import pygraphviz
import pydot
import re

from networkx.drawing import nx_agraph
from collections import defaultdict
from .normalizer import Normalizer
from asm2vec.asm import BasicBlock, parse_instruction

import pdb
class FunctionCFG:
  IDENTIFIERS = "[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*"
  INLINE_ALPHA_THRESHOLD = 0.01
  INLINE_LEN_MIN = 10
  INLINE_LEN_THRESHOLD = 0.6
  normalizer = Normalizer()

  def __init__(self, function_name, cfg_map, caller = True):
    self._cfg = cfg_map[function_name]['cfg']
    self._graph = self.get_function_graph()
    self._name = function_name
    self._length = self.function_len()
    self._blocks = self.generate_function_cfg(cfg_map, caller)

  def generate_function_cfg(self, cfg_map, caller = True):
    blocks = defaultdict(lambda: BasicBlock())
    
    for block in self._graph.nodes(data = True):
      node_id = block[0]
      normalized_contents = self.normalizer.normalize(block)
      successors = self.get_block_successors(node_id)

      for i, inst in enumerate(normalized_contents):
        callee_function_name = self.check_identifiers(inst)

        if caller and callee_function_name and callee_function_name in cfg_map:
          callee = FunctionCFG(callee_function_name, cfg_map, caller = False)

          
          if callee.root() and self.inline_callee(callee, cfg_map):
            blocks[node_id].add_successor(callee.root())
            node_id = node_id + '_' + str(i)
            callee.tail().add_successor(blocks[node_id])
          else:
            parsed_instruction = parse_instruction(inst)
            blocks[node_id].add_instruction(parsed_instruction)
        else:
          parsed_instruction = parse_instruction(inst)
          blocks[node_id].add_instruction(parsed_instruction)

      for successor in successors:
        # uses default dict val if self.blocks[node_id] or self.blocks[successor] not initialized yet
        blocks[node_id].add_successor(blocks[successor])
      
    return blocks

  def root(self):
    if not self._blocks:
      return None
    else:
      for block in self._blocks.values():
        if not block._predecessors:
          return block

    return self._blocks[next(iter(self._blocks))] if self._blocks else None

  def tail(self):
    if not self._blocks:
      return None
    else:
      for block in self._blocks.values():
        if not block._successors:
          return block

  def get_block_successors(self, block):
    # edge[0] = start node, edge[1] = destination node
    return [edge[1] for edge in self._graph.out_edges(block)]

  def get_function_graph(self):
    return nx_agraph.from_agraph(pygraphviz.AGraph(self._cfg))

  def check_identifiers(self, inst):
    identifier = re.search(self.IDENTIFIERS, inst)

    if identifier:
      return identifier.group(0)[1:]
    
    return None

  def generate_pngs(self, filepath):

    def get_dot_graph(cfg):
      (graph,) = pydot.graph_from_dot_data(cfg)
      return graph

    print("\tGenerating cfg for " + self._name)
    graph = get_dot_graph(self._cfg)
    graph.write_png(filepath + self._name + '.png')   

  def function_len(self):
    length = 0

    for block in self._graph.nodes(data = True):
      normalized_contents = self.normalizer.normalize(block)
      length += len(normalized_contents)

    return length

  def inline_callee(self, callee, cfg_map):
    if (self._length < self.INLINE_LEN_MIN) or ((callee._length/self._length) < self.INLINE_LEN_THRESHOLD):
      return True
    
    in_degree = cfg_map[callee._name]['in_degree']
    out_degree = cfg_map[callee._name]['out_degree']
    alpha = out_degree/(in_degree + out_degree)

    if alpha > self.INLINE_ALPHA_THRESHOLD:
      return True

    return False