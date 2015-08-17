#!/usr/bin/env python
import collections
import extractor_util as util
import data_util as dutil
import random
import re
import os
import sys

# This defines the Row object that we read in to the extractor
parser = util.RowParser([
          ('table_id', 'text'),
          ('gene_mention_id', 'text'),
          ('gene_cell_id', 'int'),
          ('gene_entity', 'text'),
          ('gene_word_idxs', 'int[]'),
          ('pheno_mention_id', 'text'),
          ('pheno_cell_id', 'int'),
          ('pheno_entity', 'text'),
          ('pheno_word_idxs', 'int[]'),
          ('gene_cell_words', 'text[]'),
          ('gene_cell_type', 'text'),
          ('gene_cell_attributes', 'text[]'),
          ('gene_cell_xpos', 'int'),
          ('gene_cell_xspan', 'int'),
          ('gene_cell_ypos', 'int'),
          ('gene_cell_yspan', 'int'),
          ('pheno_cell_words', 'text[]'),
          ('pheno_cell_type', 'text'),
          ('pheno_cell_attributes', 'text[]'),
          ('pheno_cell_xpos', 'int'),
          ('pheno_cell_xspan', 'int'),
          ('pheno_cell_ypos', 'int'),
          ('pheno_cell_yspan', 'int')])

# This defines the output Relation object
Relation = collections.namedtuple('Relation', [
            'id',
            'relation_id',
            'table_id',
            'gene_mention_id',
            'pheno_mention_id',
            'type',
            'is_correct'])

### DISTANT SUPERVISION ###
def supervise_relation(row, gp_dict):
  r = Relation(
        id=None,
        relation_id='%s_%s' % (row.gene_mention_id, row.pheno_mention_id),
        table_id=row.table_id,
        gene_mention_id=row.gene_mention_id,
        pheno_mention_id=row.pheno_mention_id,
        type=None,
        is_correct=None)

  # Only consider SAME ROW
  if row.gene_cell_ypos != row.pheno_cell_ypos:
    return None

  # Charite supervision- basic
  for gid in row.gene_entity.split('|'):
    for pid in row.pheno_entity.split('|'):
      if (gid, pid) in gp_dict:
        return r._replace(type='CHARITE_SUP', is_correct=True)
  return r
  
if __name__ == '__main__':
  GP_DICT = dutil.load_gp_supervision()
  for line in sys.stdin:
    row = parser.parse_tsv_row(line)
    relation = supervise_relation(row, GP_DICT)
    if relation is not None:
      util.print_tsv_output(relation)
