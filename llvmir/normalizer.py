import re
import pdb
class Normalizer:
  # ORDER MATTERS
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
    },
    {
      'regex': r"[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*",
      'sub': 'n_id',
      'llvm_type': 'named_identifier'
    },
    {
      'regex': r"i[0-9]+",
      'sub': "int_type",
      'llvm_type': "integer_type"
    },
    # {
    #   'regex': r"[%@][-a-zA-Z$._][-a-zA-Z$._0-9]*\(.*\)",
    #   'sub': 'func',
    #   'llvm_type': 'function'
    # },
    {
      'regex': r"[%@][0-9]+",
      'sub': 'un_id',
      'llvm_type': 'unnamed_identifier'
    },
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
    {
      'regex': r"^\S+:$",
      'sub': 'label_id',
      'llvm_type': 'label_id'
    },
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

# attribute groups
# begin with # (may need to inline)

  def __init__(self):
    self

  def normalize(self, lines):
    normalized_lines = []

    concat = False
    multiline = None
    for line in lines:
      if concat:
        multiline += " " + line
        
        if line.endswith("]"):
          concat = False
          line = multiline
        else:
          continue

      if line.endswith("["):
        multiline = line
        concat = True
        continue

      for sub_string in self.REGEX_SUBS:
        line = re.sub(sub_string['regex'], sub_string['sub'], line)
      
      normalized_lines.append(line)
    
    return normalized_lines