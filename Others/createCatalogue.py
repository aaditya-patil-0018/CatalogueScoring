# importing the needed modules
import json
import pandas as pd
import base64
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
images = {}

for i in range(4001):
    if f"{i}.jpeg" in imgFile:
        with open(f"flipkart_com-ecommerce_sample_images/{i}.jpeg", mode="rb") as file:
            img = file.read()
        images[i] = base64.b64encode(img).decode('utf-8')  # Encode as base64 string
        print(f"{i}: Done")

for i in range(4001):
    jsonFile["id"].append(i)
    jsonFile["product image"].append(images.get(i, nan))

with open(jsonFilename, "w") as outfile:
    json.dumps(jsonFile, indent=4)
    json.dump(jsonFile, outfile)
    # print(jsonFile)
