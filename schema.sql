-- NOTE: for greenplum compatibility, we put the DISTRIBUTED BY column first in all tables

DROP TABLE IF EXISTS cells CASCADE;
CREATE TABLE cells (
  table_id TEXT,
  cell_id INT,
  words TEXT[],
  type TEXT,
  attributes TEXT[],
  xpos INT,
  xspan INT,
  ypos INT,
  yspan INT
);

DROP TABLE IF EXISTS cells_serialized CASCADE;
CREATE TABLE cells_serialized (
  table_id TEXT,
  cell_id INT,
  words TEXT,
  type TEXT,
  attributes TEXT,
  xpos INT,
  xspan INT,
  ypos INT,
  yspan INT
);

DROP TABLE IF EXISTS tables_serialized CASCADE;
CREATE TABLE tables_serialized (
  table_id TEXT,
  cell_ids TEXT,
  words TEXT[],
  types TEXT,
  attributes TEXT[],
  xpos TEXT,
  xspans TEXT,
  ypos TEXT,
  yspans TEXT
);

DROP TABLE IF EXISTS gene_mentions CASCADE;
CREATE TABLE gene_mentions (
  table_id TEXT,
  mention_id TEXT,
  cell_id INT,
  entity TEXT,
  word_idxs INT[],
  type TEXT,
  is_correct BOOLEAN,
  id BIGINT
);

DROP TABLE IF EXISTS pheno_mentions CASCADE;
CREATE TABLE pheno_mentions (
  table_id TEXT,
  mention_id TEXT,
  cell_id INT,
  entity TEXT,
  word_idxs INT[],
  type TEXT,
  is_correct BOOLEAN,
  id BIGINT
);

DROP TABLE IF EXISTS genepheno_candidates CASCADE;
CREATE TABLE genepheno_candidates (
  table_id TEXT,
  relation_id TEXT,
  gene_mention_id TEXT,
  pheno_mention_id TEXT,
  type TEXT,
  is_correct BOOLEAN,
  id BIGINT
);

DROP TABLE IF EXISTS genepheno_features CASCADE;
CREATE TABLE genepheno_features (
  table_id TEXT,
  relation_id TEXT,
  feature TEXT
);

DROP TABLE IF EXISTS is_genepheno_relation CASCADE;
CREATE TABLE is_genepheno_relation (
  table_id TEXT,
  relation_id TEXT,
  id BIGINT,
  label BOOLEAN
);
