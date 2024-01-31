# importing all the needed modules
from Catalogue import Catalogue
import json
import re

class attributesScoring:
    
    def __init__(self, filename):
        self.catalogue = Catalogue()
        self.catalogueData = self.catalogue.open(filename)
        self.catalogueAttributes = {}

    def check(self):
        self.catalogueInformation = self.catalogue.information()
        attributeList = []
        for attribute in self.catalogueInformation:
            cleanAttribute = re.sub(r'[^a-zA-Z0-9]', '', attribute).lower()
            attributeList.append(cleanAttribute)
            self.identifyAttribute(cleanAttribute)
    
    def identifyAttribute(self, attribute):
        essentialAttributesFile = "essentialColumns.json"
        with open(essentialAttributesFile, 'r') as file:
            essentialAttributes = json.load(file)
        for attributes in essentialAttributes["columns"]:
            for token in essentialAttributes["columns"][attributes]:
                if token == attribute or attribute in token or token in attribute:
                    print(attribute + " | " + attributes + " | " + token)
                    return True
        print(attribute)
        return False

if __name__ == "__main__":
    # filename = input("Enter the Filename of Catalogue")
    filename = "Datasets/flipkart-earphone-details.csv"
    CatalogueCheck1 = attributesScoring(filename=filename)
    CatalogueCheck1.check()
