import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from table_struct import TableGrid
from simple_extractors import *


if __name__ == '__main__':
  """Script to tag & filter the tables for / based on entities (G, P, GV)"""
  DICTS = load_dicts()
  for line in sys.stdin:
    num_g = 0
    num_p = 0
    table = TableGrid(json.loads(line))

    # tag & collect any G,P entities in the table wrapper elements
    table.before, table.before_entities = tag_all(table.before, 'b', DICTS)
    table.after, table.after_entities = tag_all(table.after, 'a', DICTS)

    # tag & collect any G,P entities in the table cells
    for i,cell in enumerate(table.cells):
      cell.content, cell.entities = tag_all(cell.content, i, DICTS)

    # filter: both g and p
    table_entities = table.get_all_entities()
    #if 'g' in table_entities and 'p' in table_entities:
    if 'v' in table_entities:
      print json.dumps(table.to_json_dict())
