import sys
sys.path.append('../../src')
import json
from collections import defaultdict
from objects import TableGrid
from simple_extractors import tag_all
import util


if __name__ == '__main__':
  """Script to tag & filter the tables for / based on entities (G, P, GV)"""
  DICTS = load_dicts()
  for line in sys.stdin:
    num_g = 0
    num_p = 0
    table = TableGrid(json.loads(line))

    # tag & collect any G,P entities in the table cells
    for i,cell in enumerate(table.cells):
      cell.content, cell.entities = tag_all(cell.content, i, DICTS)

    # get all entities, for optionally filtering output tables
    entities = {}
    for cell in table.cells:
      entities = util.merge_list_dicts(entities, cell.entities)

    # filter: both g and p
    if 'g' in entities and 'p' in entities:
      print json.dumps(table.to_dict())
