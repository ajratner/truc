import json
import copy


def merge_list_dicts(a_in, b_in):
  """
  Merges two dictionaries with the following rule set:
    - if both dicts have same key and both values are lists, concatenate
    - else b replaces a if conflict
  """
  a = copy.deepcopy(a_in)
  b = copy.deepcopy(b_in)
  for k,v in b.iteritems():
    if type(v) in [list,tuple] and k in a and type(a[k]) in [list,tuple]:
      a[k] = list(a[k]) + list(v)
    else:
      a[k] = v
  return a


class TableCell:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid cell format"""
    self.content = obj['c'].encode('utf8')
    self.attributes = obj.get('attrs', [])
    self.entities = obj.get('ents', {})
    self.x = [int(x) for x in obj['x']] if type(obj['x']) is list else [int(obj['x'])]*2
    self.y = [int(y) for y in obj['y']] if type(obj['y']) is list else [int(obj['y'])]*2

  def _add_to_json_dict(self, obj, key, short_name):
    v = self.__dict__[key]
    if len(v) > 0:
      obj[short_name] = v

  def to_json_dict(self):
    obj = {'c':self.content}
    self._add_to_json_dict(obj, 'attributes', 'attrs')
    self._add_to_json_dict(obj, 'entities', 'ents')
    obj['x'] = self.x[0] if self.x[0] == self.x[1] else self.x
    obj['y'] = self.y[0] if self.y[0] == self.y[1] else self.y
    return obj

  def __repr__(self):
    return '<TableCell content="%s" @ x=%s, y=%s>' % (self.content, self.x, self.y)

  
class TableGrid:
  def __init__(self, obj):
    """Initialized from JSON object / dict in tableGrid format"""
    self.id = obj['id']
    self.cells = [TableCell(cell) for cell in obj['cells']]
    self._sort_cells()
    self.before = obj.get('bef', '').encode('utf8')
    self.after = obj.get('aft', '').encode('utf8')
    self.before_entities = obj.get('bef-ents', {})
    self.after_entities = obj.get('aft-ents', {})
    self.supervision = obj.get('sup', {})

  def get_all_entities(self):
    ents = merge_list_dicts(self.before_entities, self.after_entities)
    for cell in self.cells:
      ents = merge_list_dicts(ents, cell.entities)
    return ents

  def _sort_cells(self):
    """Sorts cells in row-major order"""
    R = len(self.cells)
    self.cells.sort(key=lambda c : c.y[0]*R + c.x[0])

  def _add_to_json_dict(self, obj, key, short_name):
    v = self.__dict__[key]
    if len(v) > 0:
      obj[short_name] = v

  def to_json_dict(self):
    obj = {"id": self.id, "cells": [cell.to_json_dict() for cell in self.cells]}
    self._add_to_json_dict(obj, 'before', 'bef')
    self._add_to_json_dict(obj, 'after', 'aft')
    self._add_to_json_dict(obj, 'before_entities', 'bef-ents')
    self._add_to_json_dict(obj, 'after_entities', 'aft-ents')
    self._add_to_json_dict(obj, 'supervision', 'sup')
    return obj

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
      if max_n is not None and i > max_n:
        break
      tables.append(TableGrid(json.loads(line.strip())))
  return tables
