import json
import copy

class Relation:
  def __init__(self, table_grid, 

# Note: a previous version (table_struct.py) took efforts to condense the JSON output...
# this seemed to complicate things but if space is an issue this can be brought back

class TableCell:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid cell format"""
    self.content = obj['content'].encode('utf8')
    self.attributes = obj.get('attributes', [])
    self.entities = obj.get('entities', [])

    # TYPE can be: PRE, POST, CELL
    self.type = obj.get('type', 'CELL')

    # Coordinates are in [START, END] format
    self.x = obj.get('x')
    self.y = obj.get('y')

  def __repr__(self):
    return '<TableCell content="%s" @ x=%s, y=%s>' % (self.content, self.x, self.y)

class TableGrid:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid format"""
    self.id = obj['id']
    self.cells = [TableCell(cell) for cell in obj['cells']]
    self._sort_cells()

  def _sort_cells(self):
    """Sorts cells in row-major order"""
    R = len(self.cells)
    self.cells.sort(key=lambda c : c.y[0]*R + c.x[0])

  def to_dict(self):
    obj = self.__dict__
    obj['cells'] = [cell.__dict__ for cell in self.cells]
    return obj

  def __repr__(self):
    return "<TableGrid for %s: %s cells>" % (self.id, len(self.cells))

def load_table_grids(filepath, max_n=None, offset=None):
  """Load a list of TableGrid objects from file w/ one JSON object per line"""
  tables = []
  with open(filepath, 'rb') as f:
    for i,line in enumerate(f):
      if offset is not None and i < offset:
        continue
      if max_n is not None and i >= max_n:
        break
      tables.append(TableGrid(json.loads(line.strip())))
  return tables
