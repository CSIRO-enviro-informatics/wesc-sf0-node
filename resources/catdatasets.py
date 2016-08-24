import os
import json
import sys


dataimportcfg_fname = 'dataimportcfg.json'

dataimportcfg_file_exists = False
if os.path.isfile(dataimportcfg_fname):
   dataimportcfg_file_exists = True
   json_data=open(dataimportcfg_fname)
else:
   print dataimportcfg_fname + " DOES NOT exist"
   sys.exit(1)

data = json.load(json_data)
json_data.close()

#loop over catalog and if selectedimport file exists, 
#then import whatever is there
#otherwise import everything in the catalog
arrDataset = []
for anImport in data["imports"]:
   arrDataset.append(anImport['id'])

print ' '.join(arrDataset)
