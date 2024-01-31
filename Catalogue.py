# importing all the needed modules
import pandas as pd

# creating a class for handling Catalogue
class Catalogue:

    def __init__(self):
        # print("Catalogue Management Class: Catalogue.py")
        pass

    def open(self, filename):
        fileExtension = filename.split(".")[-1]
        if fileExtension == "csv":
            # reading the csv file
            self.CatalogueData = pd.read_csv(filename)
            # returning the database
            return self.CatalogueData
        
        elif fileExtension == ".json":
            pass
        
        elif fileExtension == "xlsx":
            pass

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
    print(catalogue.information())
