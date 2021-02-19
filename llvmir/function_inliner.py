import llvmlite.binding as llvm
import re

from collections import Counter

IDENTIFIERS = "[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*"
FUNC_NAME = "CFG for \'(.+?)\' function"

def get_cfg_map(functions):
  cfg_map = {}

  for raw_func in functions:
    cfg = get_cfg(raw_func)
    function_name = get_function_name(cfg)
    function_callees = get_callees(cfg)
    function_out_degree = get_out_degree(function_callees)
    cfg_map[function_name] = {
      'cfg': cfg,
      'callees': function_callees,
      'out_degree': function_out_degree
    }

  return cfg_map

def get_cfg(func):
  return llvm.get_function_cfg(func, show_inst=True)

def get_function_name(cfg):
  return re.search(FUNC_NAME, cfg).group(1)

def get_callees(cfg):
  ids = re.findall(IDENTIFIERS, cfg)
  callees = dict(Counter(ids).items())

  callees_parsed = {}
  for callee, count in callees.items():
    callees_parsed[callee[1:]] = count

  return callees_parsed

def get_out_degree(ids):
  return sum(ids.values())

def get_in_degree_from_map(cfg_map):
  callees = []

  for function,value in cfg_map.items():
    callees.append(value['callees'])
  
  counter = Counter()
  for d in callees:
    counter.update(d)

  function_in_degrees = dict(counter)

  for function in cfg_map:
    if function not in function_in_degrees:
      cfg_map[function]['in_degree'] = 0
    else:
      cfg_map[function]['in_degree'] = function_in_degrees[function]

  return cfg_map
  
