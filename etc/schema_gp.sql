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
) DISTRIBUTED BY (table_id);

DROP TABLE IF EXISTS gene_mentions CASCADE;
CREATE TABLE gene_mentions (
  id BIGINT,
  mention_id TEXT,
  table_id TEXT,
  cell_id INT,
  word_idxs INT[],
  entity TEXT,
  type TEXT,
  is_correct BOOLEAN
) DISTRIBUTED BY (table_id);

DROP TABLE IF EXISTS pheno_mentions CASCADE;
CREATE TABLE pheno_mentions (
  id BIGINT,
  mention_id TEXT,
  table_id TEXT,
  cell_id INT,
  word_idxs INT[],
  entity TEXT,
  type TEXT,
  is_correct BOOLEAN
) DISTRIBUTED BY (table_id);

DROP TABLE IF EXISTS genepheno_relations CASCADE;
CREATE TABLE genepheno_relations (
  id BIGINT,
  relation_id TEXT,
  table_id TEXT,
  gene_mention_id TEXT,
  pheno_mention_id TEXT,
  type TEXT,
  is_correct BOOLEAN
) DISTRIBUTED BY (table_id);
