# importing all the needed modules
from Catalogue import Catalogue
from attributesScoring import attributesScoring
import cv2
import numpy as np
import os

class imageScoring:

    def __init__(self, CatalogueName, CatalogueData, CatalogueInformation):
        self.catalogueName = CatalogueName
        self.catalogueData = CatalogueData
        self.catalogueInformation = CatalogueInformation 
        self.imageColumnName = self.get_image_column()
        if self.imageColumnName != False:
            self.clear = 0
            self.blur = 0
            self.noImage = 0
            self.check_clarity()
            self.totalImage = len(self.catalogueData[self.imageColumnName])
            self.clearPercentage = (self.clear/self.totalImage)*100
            self.blurPercentage = (self.blur/self.totalImage)*100
            self.noImagePercentage = (self.noImage/self.totalImage)*100
            print(f"Clear Image: {round(self.clearPercentage, 2)}%")
            print(f"Blur Image: {round(self.blurPercentage, 2)}%")
            print(f"No Image Percentage: {round(self.noImagePercentage, 2)}%")
        else:
            print("No Image Column in the Catalogue!")

    def get_image_column(self):
        attributes = attributesScoring(self.catalogueData, self.catalogueInformation)
        attributes.check()
        if attributes.attributesDictionary["product image"][0] == 1:
            indValue = attributes.attributeList.index(attributes.attributesDictionary["product image"][1])
            return list(self.catalogueData.columns)[int(indValue)]
        else:
            return False

    # check 1: Clarity Check
    def check_clarity(self):
        imageDirectory = f"Datasets/{self.catalogueName}_images/"
        for image in self.catalogueData[self.imageColumnName]:
            if image != "":
                image = imageDirectory + image
                image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
                laplacian_var = int(cv2.Laplacian(image, cv2.CV_64F).var())
                if laplacian_var < 40:
                    # print("Blur ", laplacian_var)
                    self.blur += 1
                else:
                    # print("Clear ", laplacian_var)
                    self.clear += 1
                # cv2.imshow("Image", image)
                # cv2.destroyAllWindows()
            else:
                self.noImage += 1

    # check 2: Correctness
        
if __name__ == "__main__":
    # filename = input("Enter the Filename of Catalogue")
    # files = os.listdir('Datasets/')
    # for n, i in enumerate(files):
    #     print(f"{n}. {i}")
    # filename = f"Datasets/{files[int(input('Enter the file number: '))]}"
    filename = "catalogue.json"
    catalogue = Catalogue()
    catalogueData = catalogue.open(filename)
    catalogueInformation = catalogue.information()
    imgScoring = imageScoring(filename, catalogueData, catalogueInformation)