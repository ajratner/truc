import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from table_struct import TableGrid
from simple_extractors import *
import data_util as dutil

if __name__ == '__main__':
  """Script to tag & filter the tables for / based on entities (G, P, GV)"""
  gp = dutil.load_gp_supervision()
  for line in sys.stdin:
    table = TableGrid(json.loads(line))
    table_entities = table.get_all_entities()
    is_correct = None
    for g in table_entities['g']:
      for p in table_entities['p']:
        if (g,p) in gp:
          is_correct = True
    if is_correct:
      print json.dumps(table.to_json_dict())
