### SCHEMA ###
cells(
  table_id    text,
  cell_id     int,
  words       text[],
  type        text,
  attributes  text[],
  xpos        int,
  xspan       int,
  ypos        int,
  yspan       int
).

cells_serialized(
  table_id    text,
  cell_id     int,
  words       text,
  type        text,
  attributes  text,
  xpos        int,
  xspan       int,
  ypos        int,
  yspan       int
).

tables_serialized(
  table_id    text,
  cell_ids    text,
  words       text[],
  types       text,
  attributes  text[],
  xpos        text,
  xspans      text,
  ypos        text,
  yspans      text
).

gene_mentions(
  table_id    text,
  mention_id  text,
  cell_id     int,
  entity      text,
  word_idxs   int[],
  type        text,
  is_correct  boolean
).

pheno_mentions(
  table_id    text,
  mention_id  text,
  cell_id     int,
  entity      text,
  word_idxs   int[],
  type        text,
  is_correct  boolean
).

genepheno_candidates(
  table_id          text,
  relation_id       text,
  gene_mention_id   text,
  pheno_mention_id  text,
  type              text,
  is_correct        boolean
).

genepheno_features(
  table_id    text,
  relation_id text,
  feature     text
).

# Inference on genepheno relations
is_genepheno_relation?(table_id text, relation_id text).

# Serialization of cells- array elements separated by "|^|"
cells_serialized(
  table_id,
  cell_id,
  ARRAY_TO_STRING(words, "|^|"),
  type,
  ARRAY_TO_STRING(attributes, "|^|"),
  xpos,
  xspan,
  ypos,
  yspan) * 
  :- cells(table_id, cell_id, words, type, attributes, xpos, xspan, ypos, yspan).

# Serialization of tables- elements separated by "|^|" unless they are arrays, then separated by "|~|"
# NOTE that it is important to specify the third argument of ARRAY_TO_STRING which specifies a default
# value for NULL- otherwise it is simply skipped causing array-length errors
tables_serialized(
  table_id,
  ARRAY_TO_STRING(ARRAY_AGG(cell_id), "|^|"),
  #ARRAY_TO_STRING(ARRAY_AGG(words), "|~|", ""),
  ARRAY_AGG(words),
  ARRAY_TO_STRING(ARRAY_AGG(type), "|^|"),
  #ARRAY_TO_STRING(ARRAY_AGG(attributes), "|~|", ""),
  ARRAY_AGG(attributes),
  ARRAY_TO_STRING(ARRAY_AGG(xpos), "|^|"),
  ARRAY_TO_STRING(ARRAY_AGG(xspan), "|^|"),
  ARRAY_TO_STRING(ARRAY_AGG(ypos), "|^|"),
  ARRAY_TO_STRING(ARRAY_AGG(yspan), "|^|")
) :- cells_serialized(table_id, cell_id, words, type, attributes, xpos, xspan, ypos, yspan).


### EXTRACTORS ###

# Gene mentions
function ext_gene_mentions over like ext_mentions_input
  returns like gene_mentions
  implementation "udf/extract_gene_mentions.py" handles tsv lines.

ext_mentions_input(table_id, cell_id, words) *
:- cells_serialized(table_id, cell_id, words, a, b, c, d, e, f).

gene_mentions :- !ext_gene_mentions(ext_mentions_input).

# Pheno mentions
function ext_pheno_mentions over like ext_mentions_input
  returns like pheno_mentions
  implementation "udf/extract_pheno_mentions.py" handles tsv lines.

pheno_mentions :- !ext_pheno_mentions(ext_mentions_input).

# Gene-Pheno relations :  Candidate extraction / distant supervision
function ext_genepheno_candidates over like ext_genepheno_candidates_input
  returns like genepheno_candidates
  implementation "udf/extract_genepheno_candidates.py" handles tsv lines.

ext_genepheno_candidates_input(
  table_id, 
  g_mention_id, gc_id, g_entity, g_is_correct, ARRAY_TO_STRING(g_word_idxs, "|^|"), 
  p_mention_id, pc_id, p_entity, p_is_correct, ARRAY_TO_STRING(p_word_idxs, "|^|"),
  gc_words, gc_type, gc_attribs, gc_xpos, gc_xspan, gc_ypos, gc_yspan,
  pc_words, pc_type, pc_attribs, pc_xpos, pc_xspan, pc_ypos, pc_yspan
) :-
  gene_mentions(table_id, g_mention_id, gc_id, g_entity, g_word_idxs, a, g_is_correct),
  pheno_mentions(table_id, p_mention_id, pc_id, p_entity, p_word_idxs, c, p_is_correct),
  cells_serialized(table_id, gc_id, gc_words, gc_type, gc_attribs, gc_xpos, gc_xspan, gc_ypos, gc_yspan),
  cells_serialized(table_id, pc_id, pc_words, pc_type, pc_attribs, pc_xpos, pc_xspan, pc_ypos, pc_yspan).

genepheno_candidates :- !ext_genepheno_candidates(ext_genepheno_candidates_input).

# Gene-Pheno relations : Feature extraction
function ext_genepheno_features over like ext_genepheno_features_input
  returns like genepheno_features
  implementation "udf/extract_genepheno_features.py" handles tsv lines.

ext_genepheno_features_input(
  relation_id, 
  relation_type, 
  table_id, 
  gc_id, ARRAY_TO_STRING(g_word_idxs, "|^|"),
  pc_id, ARRAY_TO_STRING(p_word_idxs, "|^|"),
  cell_ids, cell_words, cell_types, cell_attribs, cell_xpos, cell_xspans, cell_ypos, cell_yspans
) :-
  genepheno_candidates(table_id, relation_id, g_mention_id, p_mention_id, relation_type, a),
  gene_mentions(table_id, g_mention_id, gc_id, g_entity, g_word_idxs, b, c),
  pheno_mentions(table_id, p_mention_id, pc_id, p_entity, p_word_idxs, d, e),
  tables_serialized(table_id, cell_ids, cell_words, cell_types, cell_attribs, cell_xpos, cell_xspans, cell_ypos, cell_yspans).

genepheno_features :- !ext_genepheno_features(ext_genepheno_features_input).

# Gene-Pheno inference
is_genepheno_relation(tid, rid) :- genepheno_candidates(tid, rid, b, c, d, l)
label = l.

is_genepheno_relation(tid, rid) :-
  genepheno_candidates(tid, rid, b, c, d, l),
  genepheno_features(tid, rid, f)
weight = f
function = Imply.
