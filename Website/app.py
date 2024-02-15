# This file will be used as backend of the website
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from Catalogue import Catalogue
from imageScoring import ImageScoring
from attributesScoring import attributesScoring
from nullChecker import nullChecker

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/score", methods=["GET", "POST"])
def score():
    if request.method == "GET":
        return render_template("score.html", score="", total_score="")
    elif request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            catalogue = Catalogue()
            catalogueData = catalogue.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
            score = {"attribute score": attributesScore, "null score": nullScore, "image score": imageScore}
            attribute_score = float(score["attribute score"]["percentage"])
            null_score = float(score["null score"]["totalPercent"])
            image_score = float(score["image score"]["clear percentage"])
            # image_score = float(score["image score"]["blur percentage"]) + float(score["image score"]["no image percentage"])
            total_score = ((attribute_score + image_score) / 200) * 100
            return render_template("score.html", score=score, total_score=total_score)

if __name__ == "__main__":
    app.run(debug=True)