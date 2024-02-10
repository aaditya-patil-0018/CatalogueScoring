# importing the needed modules
import json
import pandas as pd
from numpy import nan
import os

csvFilename = "flipkart_com-ecommerce_sample.csv"
filePath = "../Datasets/"+csvFilename
jsonFilename = "catalogue.json"

csvData = pd.read_csv(filePath)
columns = ['id', 'product image', 'product name', 'product description', 'maximum retailing price', 'selling price', 'manufacturer', 'product specifications']
csvColumns = ['product_name', 'retail_price', 'discounted_price', 'description', 'brand', 'product_specifications']
data = csvData[csvColumns]

jsonFile = {}

for c in columns:
    jsonFile[c] = []

jsonFile["product name"] = list(data["product_name"])[:4001]
jsonFile["product description"] = list(data["description"])[:4001]
jsonFile["maximum retailing price"] = list(data["retail_price"])[:4001]
jsonFile["selling price"] = list(data["discounted_price"])[:4001]
jsonFile["manufacturer"] = list(data["brand"])[:4001]
jsonFile["product specifications"] = list(data["product_specifications"])[:4001]

imgFile = os.listdir("flipkart_com-ecommerce_sample_images")

for i in range(4001):
    jsonFile["id"].append(i)
    if f"{i}.jpeg" in imgFile:
        jsonFile["product image"].append(f"{i}.jpeg")
    else:
        jsonFile["product image"].append(nan)

with open(jsonFilename, "w") as outfile:
    json.dump(jsonFile, outfile)
