# importing all the needed files
import pandas as pd
import json
import os

# getting all the csv files
allFiles = os.listdir("Datasets")

# storing all csv files columns data into this jsondata
allColumnNames = {}

# mandatory column attributes
mandatoryColumnData = ["product image", "product name", "product description", "maximum retailing price", "selling price", "inventory", "product category", "manufacturer", "product specification", "key features"]

# getting all the csv files one by one
for csvFile in allFiles:
    try:
        # checking if it's the csv file only
        if csvFile.split(".")[-1] == "csv":
            # reading csv file
            data = pd.read_csv("Datasets/" + csvFile)
            # adding up the column data into the dictionary
            allColumnNames[csvFile] = list(data.columns)
            print(csvFile + "\t\u2713 Done")
    except:
        continue

# converting dictionary into the json format
jsondata = json.dumps(allColumnNames, indent=2)

# writing the json file
with open("columnsData.json", "w") as outfile:
    outfile.write(jsondata)

