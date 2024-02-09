# importing all the needed modules
from Catalogue import Catalogue
from termcolor import colored, cprint   
import os
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
        self.attributeList = []
        self.readEssentialAttributes()
        for attribute in self.catalogueInformation:
            cleanAttribute = re.sub(r'[^a-zA-Z0-9]', '', attribute).lower()
            self.attributeList.append(cleanAttribute)
            self.identifyAttribute(cleanAttribute)

    def readEssentialAttributes(self):
        # Opening and Reading File
        with open(self.essentialAttributesFile, 'r') as file:
            self.essentialAttributes = json.load(file)
        for attributes in self.essentialAttributes["columns"]:
            self.attributesDictionary[attributes] = [0]
    
    def identifyAttribute(self, attribute):
        for attributes in self.essentialAttributes["columns"]:
            for token in self.essentialAttributes["columns"][attributes][0]:
                if token == attribute or attribute in token: # or token in attribute:
                    # if token == # here we would check the datatype of the essential attribute matches data's
                    # print(attribute)
                    self.attributesDictionary[attributes][0] = 1
                    self.attributesDictionary[attributes].append(attribute)
                    return True
        return False

    def score(self):
        total = 0
        score = 0
        self.check()
        for attribute in self.attributesDictionary:
            total += 1
            if self.attributesDictionary[attribute][0] == 1:
                score += 1
        print("")
        cprint(f"-> Score: {score}/{total}", "black", "on_light_cyan")
        print("\n----------------")
        cprint("Recommendations:", "light_yellow")
        print("----------------")
        self.recommendation()

    def recommendation(self):
        columnNamedProperly = []
        for attribute in self.attributesDictionary:
            if self.attributesDictionary[attribute][0] == 0:
                print(colored(f"Add: {attribute.capitalize()}", color="light_green"))
            elif self.attributesDictionary[attribute][0] == 1:
                columnNamedProperly.append(self.attributesDictionary[attribute][1])

        for attribute in self.attributeList:
            if attribute not in columnNamedProperly:
                print(colored(f"Rename: {attribute} [optional]", color="light_red"))
            elif "unname" in attribute.lower():
                print(colored(f"Remove: {attribute}", color="light_red"))

if __name__ == "__main__":
    # filename = input("Enter the Filename of Catalogue")
    files = os.listdir('Datasets/')
    for n, i in enumerate(files):
        print(f"{n}. {i}")
    filename = f"Datasets/{files[int(input('Enter the file number: '))]}"
    CatalogueCheck1 = attributesScoring(filename=filename)
    # CatalogueCheck1.check()
    CatalogueCheck1.score()
