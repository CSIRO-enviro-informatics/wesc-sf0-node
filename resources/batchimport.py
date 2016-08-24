import os
import json
import subprocess

from pprint import pprint
json_data=open('dataimportcfg.json')

data = json.load(json_data)
pprint(data)
json_data.close()
geoserver_db_name = "geoserver"
geoserver_db_user = "geoserver-admin"

for anImport in data["imports"]:
    filename = anImport["etlgenerate"]
    path = os.path.dirname(filename)
    os.chdir(path)
    subprocess.call(["python", anImport["etlgenerate"]])
    subprocess.call(["/usr/bin/psql", "-h",  "localhost", "-d", geoserver_db_name, "-U", geoserver_db_user, "-w", "-f", anImport["etlscript"]])
    pprint(anImport)
    pprint("\n")
