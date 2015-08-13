"""Miscellaneous shared tools for maniuplating data used in the UDFs"""
from collections import defaultdict, namedtuple
import os
import re
import sys

APP_HOME = os.environ['APP_HOME']


### GENE ###
def gene_symbol_to_ensembl_id_map(include_lowercase=False, constrain_to=None):
  """Maps a gene symbol from CHARITE -> ensembl ID"""
  eid_map = defaultdict(set)
  with open('%s/input/dicts/ensembl_genes.tsv' % APP_HOME, 'rb') as f:
    for line in f:
      eid, phrase, mapping_type = line.rstrip('\n').split('\t')
      if constrain_to is None or mapping_type in constrain_to:
        eid_map[phrase].add(eid)
        if include_lowercase:
          eid_map[phrase.lower()].add(eid)
  return eid_map


### PHENO ###
class Dag:
  """Class representing a directed acyclic graph."""
  def __init__(self, nodes, edges):
    self.nodes = nodes
    self.node_set = set(nodes)
    self.edges = edges  # edges is dict mapping child to list of parents
    self._has_child_memoizer = defaultdict(dict)

  def has_child(self, parent, child):
    """Check if child is a child of parent."""
    if child not in self.node_set:
      raise ValueError('"%s" not in the DAG.' % child)
    if parent not in self.node_set:
      raise ValueError('"%s" not in the DAG.' % parent)
    if child == parent:
      return True
    if child in self._has_child_memoizer[parent]:
      return self._has_child_memoizer[parent][child]
    for node in self.edges[child]:
      if self.has_child(parent, node):
        self._has_child_memoizer[parent][child] = True
        return True
    self._has_child_memoizer[parent][child] = False
    return False

def read_hpo_dag():
  with open('%s/input/dicts/hpo_phenotypes.tsv' % APP_HOME, 'rb') as f:
    nodes = []
    edges = {}
    for line in f:
      toks = line.strip(' \r\n').split('\t')
      child = toks[0]
      nodes.append(child)
      parents_str = toks[5]
      if parents_str:
        edges[child] = parents_str.split('|')
      else:
        edges[child] = []
    return Dag(nodes, edges)

def get_hpo_phenos(hpo_dag, parent='HP:0000118'):
  """Get only the children of 'Phenotypic Abnormality' (HP:0000118)."""
  return [hpo_term for hpo_term in hpo_dag.nodes
          if hpo_dag.has_child(parent, hpo_term)]

def pheno_phrase_to_hpo_id_map(hpo_dag=None):
  hpo_dag = read_hpo_dag() if hpo_dag is None else hpo_dag
  valid_hpo_ids = frozenset(get_hpo_phenos(hpo_dag))
  phenos = defaultdict(set)
  with open('%s/input/dicts/pheno_terms.tsv' % APP_HOME, 'rb') as f:
    for line in f:
      hpo_id, phrase, mapping_type = line.rstrip('\n').split('\t')
      if hpo_id in valid_hpo_ids:
        phenos[phrase].add(hpo_id)
  return phenos


### GENE-PHENO SUPERVISION ###
def load_gp_supervision(hpo_dag=None):
  """Load the gene-pheno supervision from Charite"""
  hpo_dag = read_hpo_dag() if hpo_dag is None else hpo_dag
  genes = gene_symbol_to_ensembl_id_map(include_lowercase=True)
  supervision_pairs = set()
  with open('%s/input/dicts/canon_phenotype_to_gene.map' % APP_HOME, 'rb') as f:
    for line in f:
      hpo_id, gene_symbol = line.strip().split('\t')
      hpo_ids = [hpo_id] + [parent for parent in hpo_dag.edges[hpo_id]]
      ensembl_ids = genes[gene_symbol]
      for e in ensembl_ids:
        for h in hpo_ids:
          supervision_pairs.add((e,h))
  return supervision_pairs


### GENE-VARIANT ###
# regexes from tmVar paper
# See Table 3 in http://bioinformatics.oxfordjournals.org/content/early/2013/04/04/bioinformatics.btt156.full.pdf
def comp_gv_rgx():
  # A bit silly, but copy from pdf wasn't working, and this format is simple to copy & debug...
  a = r'[cgrm]'
  i = r'IVS'
  b = r'ATCGatcgu'

  s1 = r'0-9\_\.\:'
  s2 = r'\/\>\?\(\)\[\]\;\:\*\_\-\+0-9'
  s3 = r'\/\>\<\?\(\)\[\]\;\:\*\_\-\+0-9'

  b1 = r'[%s]' % b
  bs1 = r'[%s%s]' % (b,s1)
  bs2 = r'[%s %s]' % (b,s2)
  bs3 = r'[%s %s]' % (b,s3)

  c1 = r'(inv|del|ins|dup|tri|qua|con|delins|indel)'
  c2 = r'(del|ins|dup|tri|qua|con|delins|indel)'
  c3 = r'(inv|del|ins|dup|tri|qua|con|delins|indel|fsX|fsx|fs)'

  p = r'CISQMNPKDTFAGHLRWVEYX'
  ps2 = r'[%s %s]' % (p, s2)
  ps3 = r'[%s %s]' % (p, s3)

  # regexes correspond to gene ('g') or protein ('p') variants
  GV_RGXS = [
    (r'(%s\.%s+%s%s*)' % (a,bs3,c1,bs1), 'g'),
    (r'(IVS%s+%s%s*)' % (bs3,c2,bs1), 'g'),
    (r'((%s\.|%s)%s+)' % (a,i,bs2), 'g'),
    (r'((%s\.)?%s[0-9]+%s)' % (a,b1,b1), 'g'),
    (r'([0-9]+%s%s*)' % (c2,b1), 'g'),
    (r'([p]\.%s+%s%s*)' % (ps3,c3,ps3), 'p'),
    (r'([p]\.%s+)' % ps2, 'p'),
    (r'([p]\.[A-Z][a-z]{0,2}[\W\-]{0,1}[0-9]+[\W\-]{0,1}([A-Z][a-z]{0,2}|(fs|fsx|fsX)))', 'p')]

  # Just return as one giant regex for now
  return r'|'.join([gvr[0] for gvr in GV_RGXS])
