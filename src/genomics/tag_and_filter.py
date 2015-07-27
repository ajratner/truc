import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from table_struct import TableGrid
from simple_extractors import *

if __name__ == '__main__':
  """Script to tag & filter the tables for / based on entities (G, P, GV)"""
  GENES = load_g_dict()
  PHENOS = load_p_dict()
  g_found_any = []
  p_found_any = []
  for line in sys.stdin:
    table = TableGrid(json.loads(line))
    for cell in table.cells:
      g_tagged, g_found = tag_g(cell.content, GENES)
      g_found_any.append(g_found)
      p_tagged, p_found = tag_p(cell.content, PHENOS)
      p_found_any.append(p_found)
      cell.content = p_tagged

    # if entity filter passed simply re-output same line- simple filtering
    if any(g_found_any) and any(p_found_any):
      print json.dumps(table.to_json_dict())
