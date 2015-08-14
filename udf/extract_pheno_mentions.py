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
            'entity',
            'word_idxs',
            'type',
            'is_correct'])

### CANDIDATE EXTRACTION ###
STOPWORDS = frozenset([w.strip() for w in open('%s/input/dicts/stopwords.tsv' % os.environ['APP_HOME'], 'rb')])

def keep_word(w):
  return (w.lower() not in STOPWORDS and len(w) > 2)

def extract_candidate_mentions(row, pheno_dict):
  """Extracts candidate phenotype mentions from an input row object"""
  mentions = []

  # First we initialize a list of indices which we 'split' on,
  # i.e. if a window intersects with any of these indices we skip past it
  split_indices = set()

  # split on certain characters / words e.g. commas
  split_indices.update([i for i,w in enumerate(row.words) if w in [',', ';']])

  # split on segments of more than M consecutive skip words
  seq = []
  for i,w in enumerate(row.words):
    if not keep_word(w):
      seq.append(i)
    else:
      if len(seq) > 2:
        split_indices.update(seq)
      seq = []

  # Next, pass a window of size n (dec.) over the sentence looking for candidate mentions
  MAX_LEN = 5
  for n in reversed(range(1, min(len(row.words), MAX_LEN)+1)):
    for i in range(len(row.words)-n+1):
      word_idxs = range(i,i+n)

      # Strip of any leading/trailing non-alphanumeric characters
      # TODO: Do better tokenization early on so this is unnecessary!
      words = [re.sub(r'^[^a-z0-9]+|[^a-z0-9]+$', '', w.lower()) for w in row.words[i:i+n]]

      # skip this window if it intersects with the split set
      if not split_indices.isdisjoint(word_idxs):
        continue

      # skip this window if it is sub-optimal: e.g. starts with a skip word, etc.
      if not all(map(keep_word, [words[0], words[-1]])):
        continue

      # filter out stop words
      words = filter(keep_word, words)
      
      # (1) Check for exact match (including exact match of lemmatized / stop words removed)
      # If found add to split list so as not to consider subset phrases
      phrase = ' '.join(words)
      if phrase in pheno_dict:
        mentions.append(
          Mention(
            id=None,
            mention_id='%s_%s_%s_%s' % (row.table_id, row.cell_id, word_idxs[0], word_idxs[-1]),
            table_id=row.table_id,
            cell_id=row.cell_id,
            word_idxs=word_idxs,
            entity='|'.join(list(pheno_dict[phrase])),
            type='EXACT',
            is_correct=None))
        split_indices.update(word_idxs)

  return mentions    

if __name__ == '__main__':
  PHENOS = dutil.pheno_phrase_to_hpo_id_map()
  for line in sys.stdin:
    row = parser.parse_tsv_row(line)
    mentions = extract_candidate_mentions(row, PHENOS)
    for mention in mentions:
      util.print_tsv_output(mention)
