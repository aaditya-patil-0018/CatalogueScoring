# importing all the needed modules
from Catalogue import Catalogue
import json
import re

class attributesScoring:
    
    def __init__(self, filename):
        self.catalogue = Catalogue()
        self.catalogueData = self.catalogue.open(filename)
        self.catalogueAttributes = {}
        self.essentialAttributesFile = "essentialColumns.json"
        self.attributesDictionary = {}

    def check(self):
        self.catalogueInformation = self.catalogue.information()
        attributeList = []
        self.readEssentialAttributes()
        for attribute in self.catalogueInformation:
            cleanAttribute = re.sub(r'[^a-zA-Z0-9]', '', attribute).lower()
            attributeList.append(cleanAttribute)
            self.identifyAttribute(cleanAttribute)

    def readEssentialAttributes(self):
        # Opening and Reading File
        with open(self.essentialAttributesFile, 'r') as file:
            self.essentialAttributes = json.load(file)
        for attributes in self.essentialAttributes["columns"]:
            self.attributesDictionary[attributes] = 0
    
    def identifyAttribute(self, attribute):
        for attributes in self.essentialAttributes["columns"]:
            for token in self.essentialAttributes["columns"][attributes]:
                if token == attribute or attribute in token or token in attribute:
                    self.attributesDictionary[attributes] = 1
                    # print(attribute + " | " + attributes + " | " + token)
                    return True
        return False

    def score(self):
        total = 0
        score = 0
        # print(self.attributesDictionary)
        for attribute in self.attributesDictionary:
            total += 1
            if self.attributesDictionary[attribute] == 1:
                score += 1
        print(f"-> Score: {score}/{total}")
        print("----------------")
        print("Recommendations:")
        print("----------------")
        self.recommendation()

    def recommendation(self):
        for attribute in self.attributesDictionary:
            if self.attributesDictionary[attribute] == 0:
                print(f"Add: {attribute.capitalize()}")

if __name__ == "__main__":
    # filename = input("Enter the Filename of Catalogue")
    filename = "Datasets/Amazon Books Data.csv"
    CatalogueCheck1 = attributesScoring(filename=filename)
    CatalogueCheck1.check()
    CatalogueCheck1.score()
