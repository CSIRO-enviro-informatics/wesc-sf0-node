import os
import json
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("datadir")
parser.add_argument("dataimportcfg")
parser.add_argument("dataimportsel")
args = parser.parse_args()

from pprint import pprint

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#data_dirname = '/opt/repos/test/aurin62-data'
#dataimportcfg_fname = 'dataimportcfg.json'
#dataimportsel_fname = "dataimportselection.txt"

data_dirname = args.datadir
dataimportcfg_fname = args.dataimportcfg
dataimportsel_fname = args.dataimportsel

dataimportcfg_file_exists = False
if os.path.isfile(dataimportcfg_fname):
   print dataimportcfg_fname + " exists"
   dataimportcfg_file_exists = True
   json_data=open(dataimportcfg_fname)
else:
   print dataimportcfg_fname + " DOES NOT exist"
   sys.exit(1)

#check if the data import selection is set
selected_data_file_exists = False
selected_data_lookup = {}

if os.path.isfile(dataimportsel_fname):
   selected_data_file_exists = True
   selected_data_file = open(dataimportsel_fname, "r")
   selected_data = selected_data_file.read().split()
   print "Dataset selected: "
   for dataset in selected_data:
       selected_data_lookup[dataset] = True
       print dataset
else:
   print dataimportsel_fname + " DOES NOT exist"

#catalog exists but selectedimport file may not
print "Dataset catalog: "
data = json.load(json_data)
pprint(data)
json_data.close()
geoserver_db_name = "geoserver"
geoserver_db_user = "geoserver-admin"

#loop over catalog and if selectedimport file exists, 
#then import whatever is there
#otherwise import everything in the catalog
for anImport in data["imports"]:
    if selected_data_file_exists and anImport["id"] in selected_data:
       print "Importing " + anImport['id']
       filename = anImport["etlgenerate"]
       etl_filepath = data_dirname + "/" + filename
       print "Data file path: " + etl_filepath
       path = os.path.dirname(etl_filepath)
       print "Data dir: " + path
       os.chdir(path)
       #subprocess.call(["python", anImport["etlgenerate"]])
       subprocess.call(["python", etl_filepath])
       subprocess.call(["/usr/bin/psql", "-h",  "localhost", "-d", geoserver_db_name, "-U", geoserver_db_user, "-w", "-f", anImport["etlscript"]])
       pprint(anImport)
       pprint("\n")
