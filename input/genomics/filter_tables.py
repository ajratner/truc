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
    g_found = any([tag_g(cell.content, GENES)[1] for cell in table.cells])
    p_found = any([tag_p(cell.content, PHENOS)[1] for cell in table.cells])
    #p_found = True

    # if entity filter passed simply re-output same line- simple filtering
    if g_found and p_found:
      print line.strip()
