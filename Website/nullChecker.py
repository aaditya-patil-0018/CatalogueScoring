# This program checks the null values in the catalogue

# importing the needed modules
from Catalogue import Catalogue
import pandas as pd
import json

class nullChecker:

    def __init__(self, CatalogueData, CatalogueInformation):
        self.catalogueData = CatalogueData
        self.catalogueInformation = CatalogueInformation
        # self.nullData = {
        #             "columns": {},
        #             "totalNull": 0,
        #             "totalPercent": 0
        #         }
        # self.checkNullValues()

    def checkNullValues(self):
        # print(type(self.catalogueData))
        columnsData = {}
        totalNull = 0
        totalPercent = 0
        df = self.catalogueData
        columns = df.columns
        valuesCount = 0
        for column in columns:
            totalNullValues = int(df[column].isnull().sum())
            valuesCount += int(len(df[column]))
            columnsData[column] = int(totalNullValues)
            totalNull += int(totalNullValues)
            totalPercent = 100.00 - float(round((( totalNull / valuesCount) * 100), 2))
        print({"columns": columnsData, "totalNull": totalNull, "totalPercent": totalPercent})
        return {"columns": columnsData, "totalNull": totalNull, "totalPercent": totalPercent}
    
if __name__ == "__main__":
    filename = "catalogue2.json"
    catalogue = Catalogue()
    catalogueData = catalogue.open(filename)
    catalogueInformation = catalogue.information()
    nullScoring = nullChecker(catalogueData, catalogueInformation)
    nullScoring.checkNullValues()