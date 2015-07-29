# TRUC
### Table Relation Understanding Component

### Preprocessing pipelines

#### Example: Genomics- G,P pairs
To prepare a dataset (in `TableGrid.json` format) from e.g. PLoS data (in PMC-style XML):
  1. Extract the tables from the XML -> TableGrid.json format:
  
        export TRUC_HOME=...
        cd ${TRUC_HOME}/input/pipes/xml/ && ./run.sh [INPUT_DIR] ${TRUC_HOME}/data/tables.json
  
  2. Tag and filter tables (tag all Gene or Phenotype entities, keep only tables that have both):
  
        cd ${TRUC_HOME}/src/genomics/ && ./run_parallel.sh tag_and_filter.py ${TRUC_HOME}/data/tables.json 80 1000 ${TRUC_HOME}/data/tables_filtered_tagged.json
  
  3. Supervise with Charite:
  
        cd ${TRUC_HOME}/src/genomics/ && ./run_parallel.sh supervise.py ${TRUC_HOME}/data/tables_filtered_tagged.json 80 1000 ${TRUC_HOME}/data/tables_sup.json

  4. Subsample resulting set of positive examples: `shuf -n 100 tables_sup.json > tables_sup_subset.json`
  
  5. View in Beaker Notebook (see `truc/beaker/README.md`)
