import copy
import json

def merge_list_dicts(a_in, b_in):
  """
  Merges two dictionaries with the following rule set:
    - if both dicts have same key and both values are lists, concatenate
    - else b replaces a if conflict
  """
  a = copy.deepcopy(a_in)
  b = copy.deepcopy(b_in)
  for k,v in b.iteritems():
    if type(v) in [list,tuple] and k in a and type(a[k]) in [list,tuple]:
      a[k] = list(a[k]) + list(v)
    else:
      a[k] = v
  return a

def load_table_grids(filepath, max_n=None, offset=None):
  """Load a list of TableGrid objects from file w/ one JSON object per line"""
  tables = []
  with open(filepath, 'rb') as f:
    for i,line in enumerate(f):
      if offset is not None and i < offset:
        continue
      if max_n is not None and i > max_n:
        break
      tables.append(TableGrid(json.loads(line.strip())))
  return tables
