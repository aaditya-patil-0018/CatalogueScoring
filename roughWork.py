# this code area is meant for doing rough work, trying out different things and just playing around

'''
# ADDING DATA FROM ALL THE DATA FILE TO THE COLUMNSDATA.JSON

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
'''

# MAKING THE ESSENTIALDATA.JSON FILE IN PROPER FORMAT
import json

file = "essentialColumns.json"

with open(file, 'r') as json_file:
    data = json.load(json_file)

for column in data["columns"]:
    # data["columns"[column].append(column.replace(" ", ""))
    # newList = [column.replace(" ", "")]
    newList = []
    for attribute in data["columns"][column]:
        newList.append(attribute.lower())
    data["columns"][column] = newList

with open(file, 'w') as json_file:
    json.dump(data, json_file, indent=4)        
