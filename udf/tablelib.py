#! /usr/bin/env python
from collections import namedtuple
import os
import re

Cell = namedtuple('Cell', ['id', 'words', 'type', 'attributes', 'xpos', 'xspan', 'ypos', 'yspan'])

CellSpan = namedtuple('CellSpan', ['cell', 'word_idxs'])

class Table:
  def __init__(self, ids, words, types, attribs, xpos, xspans, ypos, yspans):
    
    # Store cells in hash table to handle case where cell_id is not a set of incremental ints
    self.cells = {}
    #
    cells = map(Cell._make, zip(ids, words, types, attribs, xpos, xspans, ypos, yspans))
    for cell in cells:
      self.cells[cell.id] = cell
      self.cells[str(cell.id)] = cell

    # Get some basic properties of the table for reference
    self.width = max([cell.xpos + cell.xspan for cell in self.cells.values()]) + 1
    self.height = max([cell.ypos + cell.yspan for cell in self.cells.values()]) + 1

    # Store grid of refence to cells
    self.cell_at_array = [[None]*self.width]*self.height
    for cell in self.cells.itervalues():
      for dx in range(cell.xspan + 1):
        for dy in range(cell.yspan + 1):
          self.cell_at_array[cell.ypos+dy][cell.xpos+dx] = cell

  def cell_at(self, x, y):
    return self.cell_at_array[y][x]

STOPWORDS = frozenset([w.strip() for w in open('%s/input/dicts/stopwords.tsv' % os.environ['APP_HOME'], 'rb')])

def keep_word(w):
  return (w.lower() not in STOPWORDS and len(w) > 2)

# NOTE: this should probably be done in pre-processing...
def clean_word(w):
  return re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', w.lower().strip())

def get_ngrams(words_in, max_n=2, exclude_set=[], delim='_'):
  """
  Given a list of words, get n-grams where n <= n_max
  Also filter out stop words, lowercase, etc.
  Optionally skip certain word indexes (relative to the non-stopword-filtered list)
  """

  # Filter and clean words, keeping the exclude set indices in sync
  exclude = [i in exclude_set for i in range(len(words_in))] 
  words = []
  exclude_set = []
  for i,w in enumerate(map(clean_word, words_in)):
    if keep_word(w):
      if exclude[i]:
        exclude_set.append(len(words))
      words.append(w)

  # Get ngrams
  exclude_set = frozenset(exclude_set)
  ngrams = []
  for n in range(1, min(max_n, len(words))+1):
    for i in range(len(words)-n+1):
      if exclude_set.isdisjoint(range(i,i+n)):
        ngrams.append('_'.join(words[i:i+n]))
  return ngrams
    
def get_features(table, cell_span_1, cell_span_2):
  """
  Returns a list of feature names as strings for the relation between
  cell_1 and cell_2 in table
  """
  cell_spans = [cell_span_1, cell_span_2]
  features = set()

  # Add n-gram feature for row headers
  for i, cell_span in enumerate(cell_spans):
    row_header_cell = table.cell_at(0, cell_span.cell.ypos)
    for ngram in get_ngrams(row_header_cell.words):
      features.add('ROW_HEADER_CELL_%s[%s]' % (i, ngram))

  # Add n-gram features for column headers
  for i, cell_span in enumerate(cell_spans):
    col_header_cell = table.cell_at(cell_span.cell.xpos, 0)
    for ngram in get_ngrams(col_header_cell.words):
      features.add('COL_HEADER_CELL_%s[%s]' % (i, ngram))

  # Add n-gram features for cells
  for i, cell_span in enumerate(cell_spans):
    for ngram in get_ngrams(cell_span.cell.words, exclude_set=cell_span.word_idxs):
      features.add('CELL_%s_NGRAM[%s]' % (i, ngram))
  
  return list(features)
