import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from table_struct import TableGrid
from simple_extractors import *

def tag_all(s, g_found_any, p_found_any):
  g_tagged, g_found = tag_g(s, GENES)
  g_found_any.append(g_found)
  p_tagged, p_found = tag_p(g_tagged, PHENOS)
  p_found_any.append(p_found)
  return p_tagged

if __name__ == '__main__':
  """Script to tag & filter the tables for / based on entities (G, P, GV)"""
  GENES = load_g_dict()
  PHENOS = load_p_dict()
  for line in sys.stdin:
    table = TableGrid(json.loads(line))
    g_found_any = []
    p_found_any = []

    table.before = tag_all(table.before, g_found_any, p_found_any)
    table.after = tag_all(table.after, g_found_any, p_found_any)
    for cell in table.cells:
      cell.content = tag_all(cell.content, g_found_any, p_found_any)

    # if entity filter passed simply re-output same line- simple filtering
    if any(g_found_any) and any(p_found_any):
      print json.dumps(table.to_json_dict())
