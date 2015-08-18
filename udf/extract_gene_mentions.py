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
            'table_id',
            'mention_id',
            'cell_id',
            'entity',
            'word_idxs',
            'type',
            'is_correct',
            'id'])

### CANDIDATE EXTRACTION ###
def extract_candidate_mentions(row, gene_dict, d_in=0):
  mentions = []
  d = d_in
  for i, word in enumerate(row.words):
    
    # Strip of any leading/trailing non-alphanumeric characters
    # TODO: Do better tokenization early on so this is unnecessary!
    word = re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', word, flags=re.I)

    # Exact matches
    if len(word) > 3 and word in gene_dict:
      mentions.append(
        Mention(
          table_id=row.table_id,
          mention_id='%s_%s_%s' % (row.table_id, row.cell_id, i),
          cell_id=row.cell_id,
          word_idxs=[i],
          entity='|'.join(list(gene_dict[word])),
          type="EXACT_MATCH",
          is_correct=True,
          id=None))

    # Random negatives
    elif random.random() < 0.1 and d > 0:
      d -= 1
      mentions.append(
        Mention(
          table_id=row.table_id,
          mention_id='%s_%s_%s' % (row.table_id, row.cell_id, i),
          cell_id=row.cell_id,
          word_idxs=[i],
          entity=None,
          type="RAND_NEG",
          is_correct=False,
          id=None))
  return mentions

if __name__ == '__main__':
  gene_dict = dutil.gene_symbol_to_ensembl_id_map(include_lowercase=False, constrain_to=['CANONICAL_SYMBOL'])
  d = 0
  for line in sys.stdin:
    row = parser.parse_tsv_row(line)
    mentions = extract_candidate_mentions(row, gene_dict, d)
    d += len(filter(lambda m : m.is_correct, mentions)) - len(filter(lambda m : not m.is_correct, mentions))
    for mention in mentions:
      util.print_tsv_output(mention)
