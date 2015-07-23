# TRUC
### Table Relation Understanding Component

### Preprocessing pipelines

#### Example: Genomics
To prepare a dataset (in `TableGrid.json` format) from e.g. PLoS data (in PMC-style XML):
  1. Extract the tables from the XML -> TableGrid.json format:
  
        export TRUC_HOME=...
        cd ${TRUC_HOME}/input/pipes/xml/ && ./run.sh [INPUT_DIR] ${TRUC_HOME}/data/tables.json
  2. Filter the tables- for ex: those that contain a Gene or Phenotype entity:
  
        cd ${TRUC_HOME}/src/genomics/ && ./run_parallel.sh filter_tables.py ${TRUC_HOME}/data/tables.json 80 1000 ${TRUC_HOME}/data/tables_filtered.json
  3. Tag the entities in the tables:
  
        ./run_parallel.sh tag_entities.py ${TRUC_HOME}/data/tables_filtered.json 80 1000 ${TRUC_HOME}/data/tables_filtered_tagged.json
  4. View in Beaker Notebook
