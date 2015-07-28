from collections import defaultdict
import data_util as dutil
import re

def load_dicts():
  """Wrapper function for loading required dictionaries"""
  g = dutil.gene_symbol_to_ensembl_id_map(include_lowercase=False, constrain_to=['CANONICAL_SYMBOL'])
  p = dutil.pheno_phrase_to_hpo_id_map()
  return {'g':g, 'p':p}

def tag_all(s, sid, dicts):
  """
  Wrapper function to tag entities in correct order
  Returns the html-tagged string and a dictionary of entity lists
  """
  entities = {}
  g_tagged, g_entities = tag_g(s, sid, dicts['g'])
  if len(g_entities) > 0:
    entities['g'] = g_entities
  p_tagged, p_entities = tag_p(g_tagged, sid, dicts['p'])
  if len(p_entities) > 0:
    entities['p'] = p_entities
  return p_tagged, entities


### GENE ###

GENE_TAG_START = "G"
GENE_TAG_END = GENE_TAG_START

def tag_g(s, sid, genes):
  """
  Simple function to tag canonical gene mentions.
  Returns tagged input and non-unique entities list
  NOTE that the entity list is a list of pipe-concatenated entity matches per mention
  """
  toks = re.split(r'\s+', s)
  toks_out = []
  entities = []
  for tok in toks:
    new_tok = tok
    if len(tok) > 3 and tok in genes:
      entity = '|'.join(list(genes[tok]))
      tag_id = 'g-%s-%s' % (sid, len(entities))
      new_tok = '<%s id="%s" entity="%s">%s</%s>' % (GENE_TAG_START, tag_id, entity, tok, GENE_TAG_END)
      entities.append((entity, tag_id))
    toks_out.append(new_tok)
  return ' '.join(toks_out), entities


### PHENO ###

PHENO_TAG_START = "P"
PHENO_TAG_END = PHENO_TAG_START
STOPWORDS = frozenset([w.strip() for w in open('dicts/stopwords.tsv', 'rb')])

def keep_word(w):
  return (w.lower() not in STOPWORDS and len(w) > 2)

def tag_p(s, sid, phenos):
  """
  Simple function to tag pheno mentions.
  Returns tagged input and non-unique entities list
  NOTE that the entity list is a list of pipe-concatenated entity matches per mention
  """
  toks = re.split(r'\s+', s)
  mentions = []
  entities = []

  # First we initialize a list of indices which we 'split' on,
  # i.e. if a window intersects with any of these indices we skip past it
  split_indices = set()

  # split on certain characters / toks e.g. commas
  split_indices.update([i for i,w in enumerate(toks) if w in [',', ';']])

  # split on segments of more than M consecutive skip toks
  seq = []
  for i,w in enumerate(toks):
    if not keep_word(w):
      seq.append(i)
    else:
      if len(seq) > 2:
        split_indices.update(seq)
      seq = []

  # Next, pass a window of size n (dec.) over the sentence looking for candidate mentions
  MAX_LEN = 7
  for n in reversed(range(1, min(len(toks), MAX_LEN+1))):
    for i in range(len(toks)-n+1):
      wordidxs = range(i,i+n)
      words = [w.lower() for w in toks[i:i+n]]
      orig_phrase = ' '.join(toks[i:i+n])

      # skip this window if it intersects with the split set
      if not split_indices.isdisjoint(wordidxs):
        continue

      # skip this window if it is sub-optimal: e.g. starts with a skip word, etc.
      if not all(map(keep_word, [words[0], words[-1]])):
        continue

      # filter out stop words
      words = filter(keep_word, words)

      # (1) Check for exact match (including exact match of lemmatized / stop words removed)
      # If found add to split list so as not to consider subset phrases
      phrase = ' '.join(words)
      if phrase in phenos:
        mentions.append([orig_phrase, '|'.join(list(phenos[phrase]))])
        split_indices.update(wordidxs)
        continue

  # sub in the tagged entities
  s_out = ' '.join(toks)
  for m in mentions:
    entity = m[1]
    tag_id = 'p-%s-%s' % (sid, len(entities))
    s_out = re.sub(re.escape(m[0]), '<%s id="%s" entity="%s">%s</%s>' % (PHENO_TAG_START, tag_id, entity, m[0], PHENO_TAG_END), s_out, flags=re.I)
    entities.append((entity, tag_id))
  return s_out, entities
