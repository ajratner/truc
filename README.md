# TRUC
### Table Relation Understanding Component

### Deepdive workflows

#### Example: Genomics: G-P pairs

##### Pre-processing:
Starting with a dataset of tables from XML document data (e.g. a directory of PLoS documents in PMC-style XML):
  1. Extract the tables from the XML -> `cells.tsv` format:
  ```bash  
  cd ${APP_HOME}/input/parsers/xml/
  ./run.sh ${INPUT_XML_DIR} ${APP_HOME}/input/data/cells.tsv
  ```
  
  2. *Optional:* Filter the dataset to tables that have at least one G and P [TODO: Put this in ddl?]:
  ```SQL  
  deepdive sql
  ALTER TABLE cells RENAME TO cells_all;
  CREATE TABLE cells AS (
    SELECT * 
    FROM cells_all 
    WHERE 
      table_id IN (SELECT DISTINCT(table_id) FROM gene_mentions)
      AND table_id IN (SELECT DISTINCT(table_id) FROM pheno_mentions)
  );
  ```

##### Running:
  1. Configure `env_local.sh` correctly

  2. Compile the DDLog conf file: `./comp_ddl`.

  3. Initialize the database & load data: `deepdive initdb`
  
  4. **Run deepdive:**
    1. *To run with greenplum gpfdist: `./run_with_gp.sh`*
    2. Otherwise: `deepdive run ${PIPELINE}`
  
  6. View in Beaker Notebook (use `${TRUC_HOME}/beaker/table_viewer.bkr`; see `truc/beaker/README.md`)
