import llvmlite.binding as llvm
import pygraphviz
import random
import uuid

from networkx.drawing import nx_agraph
from .basicblock import Block
from collections import deque
from llvmir.vector import Vector
class Function:
  # vector_representation
  # execution_sequences

  def __init__(self, func):
    self.id = uuid.uuid4()
    self.vector = Vector(self.id)
    self.blocks = {}
    self.edges = []

    cfg = llvm.get_function_cfg(func, show_inst=True)
    self.graph = nx_agraph.from_agraph(pygraphviz.AGraph(cfg))

    for block in self.graph.nodes(data = True):
      self.blocks[block[0]] = Block(block, list(self.graph.edges(block[0])))
      self.edges += list(self.graph.edges(block[0]))

    self.execution_paths = self.generate_execution_paths()
    self.instr_freq_map = self.generate_instr_freq_map()

  def generate_instr_freq_map(self):
    freq_map = {}
    func_ops = []

    for block_name in self.blocks:
      for instr in self.blocks[block_name].block_contents:
        block_ops = instr.split()
        func_ops += block_ops
    
    for op in func_ops:
      if op in freq_map:
        freq_map[op] += 1 
      else:
        freq_map[op]=1
    
    return freq_map


  # generates execution traces (i.e. with with actual instructions) from execution paths
  def generate_execution_traces(self):
    traces = []

    for path in self.execution_paths:
      trace = []
      for node in path:
        trace += self.blocks[node].block_contents
      traces.append(trace)
    
    return traces

  def generate_execution_paths(self):
    paths = []
    edge_pool = set(self.edges)
    
    while len(edge_pool) != 0:
      # get 'random' edge from pool of possible edges and use as starting point to create path
      start_edge = edge_pool.pop()
      trace = deque([start_edge[0], start_edge[1]])

      up_path = self.traverse_up_graph_from_node(start_edge)
      down_path = self.traverse_down_graph_from_node(start_edge)      

      for edge in reversed(up_path):
        trace.appendleft(edge[0])
      
      for edge in reversed(down_path):
        trace.append(edge[1])
      
      paths.append(trace)
      edge_pool = edge_pool - set(up_path) - set(down_path)

    return paths

  def traverse_up_graph_from_node(self, edge):
    parent_edge = self.get_random_parent_edge(edge)
    if not parent_edge:
      return []

    path = self.traverse_up_graph_from_node(parent_edge)
    path.append(parent_edge)
    return path

  def traverse_down_graph_from_node(self, edge):
    child_edge = self.get_random_child_edge(edge)
    if not child_edge:
      return []

    path = self.traverse_down_graph_from_node(child_edge)
    path.append(child_edge)
    return path

  def get_random_parent_edge(self, edge):
    edges = list(self.graph.in_edges(edge[0]))
    if edges:
      return random.choice(edges)
    else:
      pass

  def get_random_child_edge(self,edge):
    edges = list(self.graph.out_edges(edge[1]))
    if edges:
      return random.choice(edges)
    else:
      pass