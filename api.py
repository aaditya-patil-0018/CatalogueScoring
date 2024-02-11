# API for Catalog Scoring

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

score_put_args = reqparse.RequestParser()
score_put_args.add_argument("json", type=werkzeug.datastructures.FileStorage, location='files')
score_put_args.add_argument("csv", type=werkzeug.datastructures.FileStorage, location='files')
score_put_args.add_argument("xlsx", type=werkzeug.datastructures.FileStorage, location='files')

class Scoring(Resource):
    def get(self):
        return {"message": "This is the catalogue scoring API."}

    def put(self):
        args = score_put_args.parse_args()
        json_file = args['json']
        csv_file = args['csv']
        xlsx_file = args['xlsx']
        catalogue = Catalogue()
        if json_file:
            filename = f"{str(uuid.uuid4())}.json"  # Generate a unique filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            json_file.save(file_path)  # Save the file to the upload folder
            print(f"File saved as '{filename}' in '{file_path}'")
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
            return {"attribute score": attributesScore, "null score": nullScore, "image score": imageScore}
            # return {"message": f"Received JSON File successfully."}
        elif csv_file:
            catalogueData = catalogue.open(csv_file)
            catalogueInformation = catalogue.information()
        elif xlsx_file:
            catalogueData = catalogue.open(xlsx_file)
            catalogueInformation = catalogue.information()
        else:
            return {"message": "No file received."}, 400

api.add_resource(Scoring, "/score/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
