'''
nullChecker
    This file checks the completeness of the data
    It identifies the number of null datapoints in the catalog and returns us the value.
'''

# This program checks the null values in the catalogue

# importing the needed modules
from Catalogue import Catalogue
import pandas as pd
import json

class nullChecker:

    def __init__(self, CatalogueData, CatalogueInformation):
        self.catalogueData = CatalogueData
        self.catalogueInformation = CatalogueInformation

    def checkNullValues(self):
        columnsData = {} # data to store column wise
        totalNull = 0 # total number of null values
        totalPercent = 0 # total precentage of null values
        df = self.catalogueData 
        columns = df.columns
        valuesCount = 0
        # checks every column data of the catalog
        for column in columns:
            # this will give total number of null values in that column
            totalNullValues = int(df[column].isnull().sum())
            # adding this number to total values count
            valuesCount += int(len(df[column]))
            # storing this data under column data
            columnsData[column] = int(totalNullValues)
            # incrementing total null values
            totalNull += int(totalNullValues)
            # totalPercent = float(round((( totalNull / valuesCount) * 100), 2))
        # returning the values after the calculations
        print({"columns": columnsData, "totalNull": totalNull, "totalPercent": totalPercent})
        return {"columns": columnsData, "totalNull": totalNull, "totalPercent": totalPercent}
    
if __name__ == "__main__":
    filename = "catalogue2.json"
    catalogue = Catalogue()
    catalogueData = catalogue.open(filename)
    catalogueInformation = catalogue.information()
    nullScoring = nullChecker(catalogueData, catalogueInformation)
    nullScoring.checkNullValues()
