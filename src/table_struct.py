import json

class TableCell:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid cell format"""
    self.content = obj['c'].encode('utf8')
    self.attributes = obj.get('attrs', [])
    self.x = [int(x) for x in obj['x']] if type(obj['x']) is list else [int(obj['x'])]*2
    self.y = [int(y) for y in obj['y']] if type(obj['y']) is list else [int(obj['y'])]*2

  def __repr__(self):
    return '<TableCell content="%s" @ x=%s, y=%s>' % (self.content, self.x, self.y)

  
class TableGrid:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid format"""
    self.id = obj['id']
    self.cells = [TableCell(cell) for cell in obj['cells']]

  def to_dict(self):
    return {"id":self.id, "cells":[cell.__dict__ for cell in self.cells]}

  def __repr__(self):
    return "<TableGrid for %s: %s cells>" % (self.id, len(self.cells))


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
