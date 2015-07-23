from collections import defaultdict
import data_util as dutil
import re


### GENE ###

GENE_TAG_START = "G"
GENE_TAG_END = GENE_TAG_START

def load_g_dict():
  g = defaultdict(set)
  with open('dicts/ensembl_genes.tsv', 'rb') as f:
    for line in f:
      ensembl_id, phrase, mapping_type = line.rstrip('\n').split('\t')
      if mapping_type == 'CANONICAL_SYMBOL':
        g[phrase].add(ensembl_id)
  return g

def tag_g(s, genes):
  """Simple function to tag canonical gene mentions- also returns whether any found"""
  toks = re.split(r'\s+', s)
  toks_out = ['<%s entity="%s">%s</%s>' % (GENE_TAG_START, '|'.join(list(genes[tok])), tok, GENE_TAG_END) if tok in genes else tok for tok in toks]
  return ' '.join(toks_out), not (toks == toks_out)


### PHENO ###

PHENO_TAG_START = "P"
PHENO_TAG_END = PHENO_TAG_START

STOPWORDS = frozenset([w.strip() for w in open('dicts/stopwords.tsv', 'rb')])

def load_p_dict():
  hpo_dag = dutil.read_hpo_dag('dicts/hpo_phenotypes.tsv')
  valid_hpo_ids = frozenset(dutil.get_hpo_phenos(hpo_dag))
  p = defaultdict(set)
  with open('dicts/pheno_terms.tsv', 'rb') as f:
    for line in f:
      hpo_id, phrase, mapping_type = line.rstrip('\n').split('\t')
      if hpo_id in valid_hpo_ids:
        p[phrase].add(hpo_id)
  return p

def keep_word(w):
  return (w.lower() not in STOPWORDS and len(w) > 2)

def tag_p(s, phenos):
  """Simple function (reduced from version in dd-genomics) to tag pheno mentions- also
  returns whether any were found"""
  toks = re.split(r'\s+', s)
  mentions = []

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
    s_out = re.sub(re.escape(m[0]), '<%s entity="%s">%s</%s>' % (PHENO_TAG_START, m[1], m[0], PHENO_TAG_END), s_out, flags=re.I)
  return s_out, len(mentions) > 0
