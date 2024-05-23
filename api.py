'''
API (Appliation Programming Interface)
    This file is the Programming Interface using which Buyer/Seller App onboard the catalog and score them.
    This is the main file which will be available to the developers to use.
'''

# API for Catalog Scoring

'''
    ToDo:
        (Here user are the seller applications)
        => Create the user management for getting the API
            -> Add the API Key Feature
            -> Add the Developer Sign in & Sign up option
            -> Give unique id for identifying every user
        => Create Clear, Professional and Beautiful API Documentation
        => Create the well organized Database for the storage of API Database
        => Create and share the unique id for every catalog that user score
        => Using this unique id, user can directly check for the score and recommendations
        => Create route for recommendation option for the catalog
        => Get the user category, Optinal Columns specified by the user as the mandatory critical attributes
'''

# importing the needed modules
import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import werkzeug
import uuid
import pandas as pd
from Catalogue import Catalogue
from attributesScoring import attributesScoring
from nullChecker import nullChecker
from imageScoring import ImageScoring
import json

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# creating the arguments to add
score_put_args = reqparse.RequestParser()
score_put_args.add_argument("json", type=werkzeug.datastructures.FileStorage, location='files')
score_put_args.add_argument("csv", type=werkzeug.datastructures.FileStorage, location='files')
score_put_args.add_argument("xlsx", type=werkzeug.datastructures.FileStorage, location='files')

class Scoring(Resource):
    
    # when the get request is made this function is executed
    def get(self):
        return {"message": "This is the catalogue scoring API."}

    # when the put request is made this function is executed
    def put(self):
        
        # parsing the arguments passed
        args = score_put_args.parse_args()
        
        # getting the arguments that have been passed
        json_file = args['json']
        csv_file = args['csv']
        xlsx_file = args['xlsx']

        # creating the catalogue class object
        catalogue = Catalogue()

        # as per the type of file is passed actions are performed
        # if json file is passed
        if json_file:
            
            # ToDo: Create the function to save the file with an unique filename
            # setting the file name & saving it to the uplaods directory
            filename = f"{str(uuid.uuid4())}.json"  # Generate a unique filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            json_file.save(file_path)  # Save the file to the upload folder
            print(f"File saved as '{filename}' in '{file_path}'")
        
            # ToDo: Create the function to get the score of the catalog
            # opening the catlogue file & getting it's information
            catalogueData = catalogue.open(f"{file_path}")
            catalogueInformation = catalogue.information()
            
            # attributes score
            attributesScore = attributesScoring(catalogueData, catalogueInformation)
            attributesScore = attributesScore.score()
            
            # null data score
            nullScore = nullChecker(catalogueData, catalogueInformation)
            nullScore = nullScore.checkNullValues()
            
            # image data score
            imageScore = ImageScoring(catalogueData)
            imageScore = imageScore.check_clarity()
            
            # returns the score details
            return {"attribute score": attributesScore, "null score": nullScore, "image score": imageScore}
        
        # if csv file is passed
        elif csv_file:
            catalogueData = catalogue.open(csv_file)
            catalogueInformation = catalogue.information()
        
        # if xlsx (excel) file is passed
        elif xlsx_file:
            catalogueData = catalogue.open(xlsx_file)
            catalogueInformation = catalogue.information()
        else:
            return {"message": "No file received."}, 400

# adding the path for scoring
api.add_resource(Scoring, "/score/")

# this condition is only true when this file is runned independently
if __name__ == "__main__":
    app.run(debug=True, port=8000)
