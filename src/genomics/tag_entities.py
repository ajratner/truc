import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from table_struct import TableGrid
from simple_extractors import *

if __name__ == '__main__':
  """Script to filter the tables based on presence of certain entities (G, P, GV)"""
  GENES = load_g_dict()
  PHENOS = load_p_dict()
  for line in sys.stdin:
    table = TableGrid(json.loads(line))
    for cell in table.cells:
      cell.content = tag_p(tag_g(cell.content, GENES)[0], PHENOS)[0]
    print json.dumps(table.to_json_dict())
