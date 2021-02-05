import re

class Normalizer:
  REGEX_SUBS = [
    {
      'regex': r"c\".*\"",
      'sub': 'str',
      'llvm_type': 'string'
    },
    {
      'regex': r";.*",
      'sub': '',
      'llvm_type': 'comment'
    },
    {
      'regex': r".*=",
      'sub': 'result',
      'llvm_type': 'result'
    }
    # {
    #   'regex': r"[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*\(.*\)",
    #   'sub': 'func',
    #   'llvm_type': 'function'
    # },
    # {
    #   'regex': r"[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*",
    #   'sub': 'n_id',
    #   'llvm_type': 'named_identifier'
    # },
    {
      'regex': r"[%@][0-9]+",
      'sub': 'un_id',
      'llvm_type': 'unnamed_identifier'
    },
    # {
    #   'regex': r"i[0-9]+",
    #   'sub': 'int',
    #   'llvm_type': 'integer'
    # },
    {
      'regex': r"[-a-zA-Z0-9]+\*+",
      'sub': 'ptr',
      'llvm_type': 'pointer1'
    },
    {
      'regex': r"\[\w+\sx\s\w+\]\*+",
      'sub': 'ptr',
      'llvm_type': 'pointer2'
    },
    {
      'regex': r"\s[-]*[0-9]+",
      'sub': ' cons',
      'llvm_type': 'constant1'
    },
    {
      'regex': r"\[-*[0-9]+\s",
      'sub': '[cons ',
      'llvm_type': 'constant2'
    },
    {
      'regex': r"![0-9]+",
      'sub': 'm_data',
      'llvm_type': 'metadata'
    },
    # {
    #   'regex': r"\w+label[\w\.-]+:",
    #   'sub': 'label',
    #   'llvm_type': 'label'
    # },
    {
    'regex': r"({|}|,|\(|\)|\[|\])",
    'sub': '',
    'llvm_type': 'chars'
    },
    {
    'regex': r"\s+",
    'sub': ' ',
    'llvm_type': 'space'   
    }
  ]

  def __init__(self):
    self

  def normalize(self, lines):
    normalized_lines = []

    for line in lines:
      for sub_string in self.REGEX_SUBS:
        line = re.sub(sub_string['regex'], sub_string['sub'], line)
      
      normalized_lines.append(line)
    
    return normalized_lines