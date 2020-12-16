# WESC Data Node deployment

This repository provides a standardised method for deploying a Spatial Information Services Stack (SISS) configured
for WESCML (http://wescml.org) for SF-0.

## Pre-requisite:
wesc-sf0-node requires running on a Linux environment supporting  Docker. This package has been tested using Ubuntu Linux 14.10.

In order to use wesc-sf0-node, first install:
- [docker.io](http://docker.io)
- [csiro_env/geoserver](https://github.com/CSIRO-enviro-informatics/docker-geoserver/) - clone and build from  https://github.com/CSIRO-enviro-informatics/docker-geoserver/


## Run
Execute the ./run.sh script

Once the run script finishes, you should have a tailored SISS stack (PostgreSQL DB, Geoserver and Apache instances configured
for WESCML) running. 
To test if this is working - in a browser try:
 https://localhost:8110/geoserver


## Advanced

If you need to co-ordinate multiple wesc node deployments, this repo has text files to specify the details.

### dataselection.txt
- This file takes tab-separated parameters (\<name\> \<etl-config id\> \<exposed port number\>)  each row and deploy a node
- To add a new node, simply add a new row with details to the ETL files and port numbers
- Example: 
sydney-ex       combinedmeterreadings-sydneywater-lga   8110


### dataimportcfg.txt
- This file contains the etl-config details for each deployment and contains details for 4 fields:
  * etl-config id. This is used to map a node with the spcific wesc element - combinedmeterreadings, watersupply or electricitysupply
  * name. Description for the etl-config
  * etlgenerate. This points to relative path to the directory containing the etl script
  * etlscript. This points to relative path to the SQL etl script as output.
- Example:
    {
        "id": "combinedmeterreadings-sydneywater-lga",
        "name": "Example Sydney Consumption Data for water",
        "etlgenerate": "example/example-sydney-lga-etl.py",
        "etlscript": "combinedmeterreadings-sydney-lga.sql"
    },


## Suggested citation

Yu, Jonathan; Leighton, Ben; Mirza, Fareed; Singh, Ramneek. [Tools for enabling rapid deployment of water and energy consumption and supply data services](http://www.mssanz.org.au/modsim2015/C8/yu.pdf). In: MODSIM 2015; 29/11/15 to 4/12/15; Gold Coast, Queensland, Australia. Modelling and Simulation Society of Australia and New Zealand (MSSANZ); 2015. pp. 781-787.

## Related papers

- Simons, Bruce; Yu, Jonathan (2015): WESCML Information Model. v1. CSIRO. Data Collection. [http://doi.org/10.4225/08/574D1DEEA50DD](http://doi.org/10.4225/08/574D1DEEA50DD)
- Simons, Bruce; Yu, Jonathan; Leighton, Benjamin (2016): [WESCML: A Data Standard for Exchanging Water and Energy Supply and Consumption Data](http://dx.doi.org/10.1016/j.proeng.2016.07.451), 12th International Hydroinformatics Conference, Incheon, South Korea, August 2016., IWA. [dx.doi.org/10.1016/j.proeng.2016.07.451](http://dx.doi.org/10.1016/j.proeng.2016.07.451)
- Yu, Jonathan; Lipkin, Felix; Moglia, Magnus. [Novel spatial analysis of residential resource consumption via the Melbourne train network](http://www.mssanz.org.au/modsim2015/M4/yu.pdf). In: Weber, T.; McPhee, M.J.; Anderssen, R.S., editor/s. MODSIM 2015; 29/11/15 to Friday 4/12/15; Gold Coast, Queensland, Australia. Modelling and Simulation Society of Australia and New Zealand (MSSANZ); 2015. p. 1188-1194.
- Yu, Jonathan; Inman, Matthew; Simons, Bruce. Protocols to integrate URBAN water data with energy and other sectors within AURIN. In: Ozwater 15; 12 - 14 May 2015; Adelaide. Australian water Association; 2015. 7pp.
