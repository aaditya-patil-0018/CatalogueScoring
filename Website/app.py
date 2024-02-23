# This file will be used as backend of the website
import os
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
from Catalogue import Catalogue
from imageScoring import ImageScoring
from attributesScoring import attributesScoring
from nullChecker import nullChecker

app = Flask(__name__)
app.secret_key = "thisisthesecretkey"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home(): 
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/catalogue', methods=["GET", "POST"])
def catalog():
    if request.method == "GET":
        if "catalog-files" in session:
            catalogue = Catalogue()
            catalogueData = catalogue.open(os.path.join(app.config['UPLOAD_FOLDER'], session["catalog-files"]))
            return render_template("catalogue.html", tableData=dict(catalogueData.to_dict()))
        else:
            return render_template("catalogue.html", tableData="")
    elif request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            session["catalog-files"] = filename
            print("session added: ", session["catalog-files"])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            catalogue = Catalogue()
            catalogueData = catalogue.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("catalogue.html", tableData=dict(catalogueData.to_dict()))

@app.route("/score", methods=["GET", "POST"])
def score():
    if "catalog-files" in session:
            filename = session["catalog-files"]
            catalogue = Catalogue()
            catalogueData = catalogue.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            catalogueInformation = catalogue.information()
            c = [i for i in catalogueInformation]
            totalColumns = len(catalogueData[c[0]])
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
            image_score = float(score["image score"]["clear percentage"])
            # image_score = float(score["image score"]["blur percentage"]) + float(score["image score"]["no image percentage"])
            nullimage = nullScore["columns"]["product image"]
            nullScore["columns"]["product image"] = imageScore["no image"]
            nullScore["totalNull"] -= nullimage
            nullScore["totalNull"] += imageScore["no image"]
            nullScore["totalPercent"] = 100.00 - round((nullScore["totalNull"] / (totalColumns * len(catalogueInformation))) * 100, 2)
            null_score = float(score["null score"]["totalPercent"])
            total_score = round(((attribute_score + image_score + null_score) / 300) * 100, 2)
            return render_template("score.html", completeness=null_score, correcteness=image_score, compliance=attribute_score,  score=score, total_score=total_score)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == "__main__":
    app.run(debug=True)