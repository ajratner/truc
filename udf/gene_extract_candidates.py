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
          ('cell_id', 'int'),
          ('words', 'text[]')])

# This defines the output Mention object
Mention = collections.namedtuple('Mention', [
            'id',
            'mention_id',
            'table_id',
            'cell_id',
            'word_idxs',
            'entity',
            'type',
            'is_correct'])

### CANDIDATE EXTRACTION ###
def extract_candidate_mentions(row, gene_dict):
  mentions = []
  for i, word in enumerate(row.words):
    
    # Strip of any leading/trailing non-alphanumeric characters
    # TODO: Do better tokenization early on so this is unnecessary!
    word = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', word, flags=re.I)

    if len(word) > 3 and word in gene_dict:
      mentions.append(
        Mention(
          id=None,
          mention_id='%s_%s_%s' % (row.table_id, row.cell_id, i),
          table_id=row.table_id,
          cell_id=row.cell_id,
          word_idxs=[i],
          entity='|'.join(list(gene_dict[word])),
          type=None,
          is_correct=None))
  return mentions

if __name__ == '__main__':
  gene_dict = dutil.gene_symbol_to_ensembl_id_map(include_lowercase=False, constrain_to=['CANONICAL_SYMBOL'])
  for line in sys.stdin:
    row = parser.parse_tsv_row(line)
    mentions = extract_candidate_mentions(row, gene_dict)
    for mention in mentions:
      util.print_tsv_output(mention)
