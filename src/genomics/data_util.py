"""Miscellaneous shared tools for maniuplating data used in the UDFs"""
from collections import defaultdict, namedtuple
import os
import re
import sys


### GENE ###

def gene_symbol_to_ensembl_id_map(include_lowercase=False, constrain_to=None):
  """Maps a gene symbol from CHARITE -> ensembl ID"""
  eid_map = defaultdict(set)
  with open('dicts/ensembl_genes.tsv', 'rb') as f:
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
  with open('dicts/hpo_phenotypes.tsv', 'rb') as f:
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
  with open('dicts/pheno_terms.tsv', 'rb') as f:
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
  with open('dicts/canon_phenotype_to_gene.map', 'rb') as f:
    for line in f:
      hpo_id, gene_symbol = line.strip().split('\t')
      hpo_ids = [hpo_id] + [parent for parent in hpo_dag.edges[hpo_id]]
      ensembl_ids = genes[gene_symbol]
      for e in ensembl_ids:
        for h in hpo_ids:
          supervision_pairs.add((e,h))
  return supervision_pairs
