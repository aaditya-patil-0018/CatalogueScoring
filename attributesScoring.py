'''
Attributes Scoring
    This is file is designed to score the attributes of the catalogue.

Why Attributes Scoring is important Required?
    Every catalogue must have certian attributes to make it complete and sensable.
    Attributes like: Name, Image, Price, Description, etc. These are certain Essential attributes that every catalogue file should have.
'''

# importing all the needed modules
from Catalogue import Catalogue
from termcolor import colored, cprint   
import os
import json
import re

class attributesScoring:
        
    def __init__(self, CatalogueData, CatalogueInformation):
        # self.catalogue = Catalogue()
        # self.catalogue = catalogue
        # self.catalogueData = self.catalogue.open(filename)
        
        # we get the catalogue data from the user
        self.catalogueData = CatalogueData
        # we get the catlaogue information from the user {columnname: dataype}
        self.catalogueInformation = CatalogueInformation
        self.catalogueAttributes = {}
        # getting the values of the essential columns (attributes) that the catalogue should contain
        self.essentialAttributesFile = "essentialColumns.json"
        self.attributesDictionary = {}
        
        # self.score()

    def check(self):
        '''
            This file checks for the clean attribute names
                => This file checks the naming style of the attribute name
                => This file makes sure that the column names 
        '''
        # self.catalogueInformation = self.catalogue.information()
        self.attributeList = []
        # this function would read all the essentialAttributes specified in the essentialColumns.json file
        self.readEssentialAttributes()
        # looping through all the attributes in the catlogue passed
        for attribute in self.catalogueInformation:
            # converting the passed column data in the form of clean way
            cleanAttribute = re.sub(r'[^a-zA-Z0-9]', '', attribute).lower()
            # addinf the attribute name to attributeList for marking that it has been traversed
            self.attributeList.append(cleanAttribute)
            # identifying and checking the attirbute is essential and needed column or not
            self.identifyAttribute(cleanAttribute)

    def readEssentialAttributes(self):
        '''
            This file reads the essentialColumns.json file and it reads & adds the data to the
                => self.essentialAttributes : json Dictionary that stores all the essential attributes data
                => self.attributesDictionary : this Dictionary keeps track of the essential attributes present in essentialAttributes dictionar as key and 0 or 1 as value based on the presence of that attribute in the catalog file
        '''
        # Opening and Reading File
        with open(self.essentialAttributesFile, 'r') as file:
            self.essentialAttributes = json.load(file)
        # creating the dictionary for storing the corresponding attribute presence in passed catlaogue file
        for attributes in self.essentialAttributes["columns"]:
            self.attributesDictionary[attributes] = [0]
    
    def identifyAttribute(self, attribute):
        '''
            This function is used to identify the presence of the attributes in the passed catalog file corresponding to the essentialAttributes that are added in the essentialColumns.json file
        '''
        # looping through all the essential attributes key:
        for attributes in self.essentialAttributes["columns"]:
            # looping through all the possilbe name of the attribute that could be potentially used in the catalog by the user
            for token in self.essentialAttributes["columns"][attributes][0]:
                # if token and attribute are the same then changing the status of the attirbutesDictionary to 1
                # appeneding the attribute present in catalog to the attributesDictionary[attribute]'s list
                if token == attribute:# or attribute in token: # or token in attribute:
                    # if token == # here we would check the datatype of the essential attribute matches data's
                    # print(colored(f"{attribute.capitalize()}", color="light_green"))
                    self.attributesDictionary[attributes][0] = 1
                    self.attributesDictionary[attributes].append(attribute)
                    # return True as the attirbute is present in the essentialColumns
                    return True
        # reuturn False as attirbute is not present in the essentialColumns
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
        recommendData = self.recommendation()
        return {"score": score, "total": total, "percentage": score*10, "recommendation": recommendData}

    def recommendation(self):
        data = {
            "add": [],
            "rename": [],
            "remove": []
        }
        columnNamedProperly = []
        for attribute in self.attributesDictionary:
            if self.attributesDictionary[attribute][0] == 0:
                print(colored(f"Add: {attribute.capitalize()}", color="light_green"))
                data["add"].append(attribute)
            elif self.attributesDictionary[attribute][0] == 1:
                columnNamedProperly.append(self.attributesDictionary[attribute][1])

        for attribute in self.attributeList:
            if attribute not in columnNamedProperly:
                print(colored(f"Rename: {attribute} [optional]", color="light_red"))
                data["rename"].append(attribute)
            elif "unname" in attribute.lower():
                print(colored(f"Remove: {attribute}", color="light_red"))
                data["remove"].append(attribute)
        return data

if __name__ == "__main__":
    filename = input("Enter the Filename of Catalogue: ")
    '''
    files = os.listdir('Datasets/')
    for n, i in enumerate(files):
        print(f"{n}. {i}")
    filename = f"Datasets/{files[int(input('Enter the file number: '))]}"
    '''
    catalogue = Catalogue()
    catalogueData = catalogue.open(filename)
    catalogueInformation = catalogue.information()
    CatalogueCheck1 = attributesScoring(CatalogueData=catalogueData, CatalogueInformation=catalogueInformation)
    # CatalogueCheck1.check()
    CatalogueCheck1.score()
