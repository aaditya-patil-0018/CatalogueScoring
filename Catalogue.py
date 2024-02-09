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
            return json.load(open(filename))

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
