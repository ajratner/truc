# TRUC
### Table Relation Understanding Component

### Deepdive workflows

#### Example: Genomics: G-P pairs
Starting with a dataset of tables from XML document data (e.g. a directory of PLoS documents in PMC-style XML):
  1. Extract the tables from the XML -> `cells.tsv` format:
  
        export TRUC_HOME=${ABS_PATH_HERE}
        cd ${TRUC_HOME}/input/parsers/xml/
        ./run.sh [INPUT_DIR] ${TRUC_HOME}/input/data/cells.tsv
  
  2. Initialize the database & load data: `deepdive initdb`
  
  3. *Optional:* Filter the dataset to tables that have at least one G and P: `deepdive run filter_tables`
  
  4. Extract G and P mentions: `deepdive run mentions`
  
  5. Extract G-P relations: `deepdive run relations`
  
  6. View in Beaker Notebook (use `${TRUC_HOME}/beaker/table_viewer.bkr`; see `truc/beaker/README.md`)
