#!/usr/bin/env python
import collections
import extractor_util as util
import tablelib
import data_util as dutil
import random
import re
import os
import sys

# This defines the Row object that we read in to the extractor
parser = util.RowParser([
          ('relation_id', 'text'),
          ('relation_type', 'text'),
          ('table_id', 'text'),
          ('gene_cell_id', 'int'),
          ('gene_word_idxs', 'int[]'),
          ('pheno_cell_id', 'int'),
          ('pheno_word_idxs', 'int[]'),
          ('cell_ids', 'int[]'),
          ('cell_words', 'text[][]'),
          ('cell_types', 'text[]'),
          ('cell_attributes', 'text[][]'),
          ('cell_xpos', 'int[]'),
          ('cell_xspans', 'int[]'),
          ('cell_ypos', 'int[]'),
          ('cell_yspans', 'int[]')])

# This defines the output Relation object
Feature = collections.namedtuple('Feature', [
            'table_id',
            'relation_id',
            'feature'])

def get_features(row):
  f = Feature(row.table_id, row.relation_id, None)

  # Form a tablelib Table object
  table = tablelib.Table(row.cell_ids, row.cell_words, row.cell_types, row.cell_attributes, \
            row.cell_xpos, row.cell_xspans, row.cell_yspans)
  
  # Form tablelib CellSapn objects using the table + cell_ids
  gene_cell = tablelib.CellSpan(table.cells[row.gene_cell_id], row.gene_word_idxs)
  pheno_cell = tablelib.CellSpan(table.cells[row.pheno_cell_id], row.pheno_word_idxs)

  # Get the tablelib generic features
  return [f._replace(feature=feature) for feature in tablelib.get_features(table, gene_cell, pheno_cell)]
  
if __name__ == '__main__':
  for line in sys.stdin:
    row = parser.parse_tsv_row(line)
    for f in get_features(row):
      util.print_tsv_output(f)
