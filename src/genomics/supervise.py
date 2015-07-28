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

    # Supervise as true if in the Charite set
    table_entities = table.get_all_entities()
    is_correct = None
    for g, gid in table_entities['g']:
      for p, pid in table_entities['p']:
        if (g,p) in gp:
          is_correct = True

          # Add supervision to tableGrid object referencing the specific tag ids
          if 'gp' not in table.supervision:
            table.supervision['gp'] = []
          table.supervision['gp'].append((gid,pid))

    # Filter: only print out the supervised tables
    if is_correct:
      print json.dumps(table.to_json_dict())
