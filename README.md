# TRUC
### Table Relation Understanding Component

### Deepdive workflows

#### Example: Genomics: G-P pairs
Starting with a dataset of tables from XML document data (e.g. a directory of PLoS documents in PMC-style XML):
  1. Extract the tables from the XML -> `cells.tsv` format:
  
        cd ${APP_HOME}/input/parsers/xml/
        ./run.sh ${INPUT_XML_DIR} ${APP_HOME}/input/data/cells.tsv
  
  2. Compile the DDLog conf file:
  
        java -jar ${DEEPDIVE_HOME}/util/ddlog.jar compile app.ddlog > deepdive.conf

  3. Initialize the database & load data: `cd ${APP_HOME} && deepdive initdb`
  
  4. *Optional:* Filter the dataset to tables that have at least one G and P [TODO: Put this in ddl?]:
  
        deepdive sql
        ALTER TABLE cells RENAME TO cells_all;
        CREATE TABLE cells AS (
          SELECT * 
          FROM cells_all 
          WHERE table_id IN (SELECT DISTINCT(table_id) FROM gene_mentions)
            AND table_id IN (SELECT DISTINCT(table_id) FROM pheno_mentions)
        );
  
  5. Extract G and P mentions, G-P relations: `deepdive run extractions`
  
  
  7. View in Beaker Notebook (use `${TRUC_HOME}/beaker/table_viewer.bkr`; see `truc/beaker/README.md`)
