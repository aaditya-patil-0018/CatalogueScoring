# This program checks the null values in the catalogue

# importing the needed modules
from Catalogue import Catalogue
import pandas as pd
import json

class nullChecker:

    def __init__(self, CatalogueData, CatalogueInformation):
        self.catalogueData = CatalogueData
        self.catalogueInformation = CatalogueInformation
        self.nullData = {
                    "columns": {},
                    "totalNull": 0,
                    "totalPercent": 0
                }
        self.checkNullValues()

    def checkNullValues(self):
        # print(type(self.catalogueData))
        df = self.catalogueData
        columns = df.columns
        valuesCount = 0
        for column in columns:
            totalNullValues = df[column].isnull().sum()
            valuesCount += len(df[column])
            self.nullData["columns"][column] = totalNullValues
            self.nullData["totalNull"] += totalNullValues
            self.nullData["totalPercent"] = round(((self.nullData["totalNull"] / valuesCount) * 100), 2)
        print(self.nullData)
        return self.nullData

if __name__ == "__main__":
    filename = "catalogue2.json"
    catalogue = Catalogue()
    catalogueData = catalogue.open(filename)
    catalogueInformation = catalogue.information()
    nullScoring = nullChecker(catalogueData, catalogueInformation)