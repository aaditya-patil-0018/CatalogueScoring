'''
Catalogue
    This file processes and works with Catalogues.

Functions in Catalogue.py =>
    - open() : Opens the passed catalogue file in pandas json dataframe format
        - xlsx_to_json() : converts the excel data file into json file and return the data
        - csv_to_json() : converts the csv data file into json file and return the data
    - information() : return the information about the data
'''

# importing all the needed modules
import pandas as pd
import json

# creating a class for handling Catalogue
class Catalogue:

    def __init__(self):
        # print("Catalogue Management Class: Catalogue.py")
        pass

    def open(self, filename):
        fileExtension = filename.split(".")[-1]
        if fileExtension == "csv":
            return self.csv_to_json(filename)
        elif fileExtension == "xlsx":
            return self.xlsx_to_json(filename)
        elif fileExtension == "json":
            self.CatalogueData = pd.read_json(filename)
            return self.CatalogueData

    def xlsx_to_json(self, filename):
        self.CatalogueData = pd.read_excel(filename)
        columns = self.CatalogueData.columns
        jsonData = {}
        for key in columns:
            values = list(self.CatalogueData[key])
            jsonData[key] = values
        jsonData = json.dumps(jsonData, indent=4)
        return jsonData

    def csv_to_json(self, filename):
        self.CatalogueData = pd.read_csv(filename)
        columns = self.CatalogueData.columns
        jsonData = {}
        for key in columns:
            values = list(self.CatalogueData[key])
            jsonData[key] = values
        jsonData = json.dumps(jsonData, indent=4)
        return jsonData

    def information(self):
        '''
            This file returns the dictionary containing the information of the dataset
                key: column name
                value: datatypes
        '''
        try:
            # getting the columns list
            columnsList = list(self.CatalogueData.columns)
            # getting datatypes list
            dtypesList = [str(i) for i in self.CatalogueData.dtypes]
            # creating a dictionary of column name & their datatypes
            self.catalogueInformation = {}
            for i in range(len(columnsList)):
                self.catalogueInformation[columnsList[i].lower()] = dtypesList[i]
            return self.catalogueInformation
        except AttributeError:
            pass

if __name__ == "__main__":
    catalogue = Catalogue()
    filename = input("Enter Filename: ")
    catalogue.open(filename)
    # print(catalogue.information())
