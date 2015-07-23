# TRUC
### Table Relation Understanding Component

### Preprocessing pipelines

#### Example: Genomics
To prepare a dataset (in `TableGrid.json` format) from e.g. PLoS data (in PMC-style XML):
  1. Extract the tables from the XML -> TableGrid.json format:
  
        ./input/pipes/xml/run.sh [INPUT_DIR] tables.json
  2. Filter the tables- for ex: those that contain a Gene or Phenotype entity:
  
        ./src/genomics/run_parallel.sh filter_tables.py tables.json 80 1000 tables_filtered.json
  3. Tag the entities in the tables:
  
        ./src/genomics/run_parallel.sh tag_entities.py tables_filtered.json 80 1000 tables_filtered_tagged.json
  4. View in Beaker Notebook
