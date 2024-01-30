# this code area is meant for doing rough work, trying out different things and just playing around
import os
import pandas as pd
import json

all_csv_files = os.listdir()

jsondata = {}

allColumnsName = ["product image", "product name", "product description", "maximum retailing price", "selling price", "inventory", "product category", "manufacturer", "product specification", "key features"]

for csv_file in all_csv_files:
    try:
        data = pd.read_csv(csv_file)
        jsondata[csv_file] = list(data.columns)
        print(len(jsondata))        
    except:
        continue

jsondata = json.dumps(jsondata, indent=2)

with open("columnsData.json", "w") as outfile:
    outfile.write(jsondata)
