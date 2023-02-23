import glob
import os

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import classification_test_model
import test_model
import geo_coding
from flask_cors import CORS
import time

import utils_draw_polygons
import json

app = Flask(__name__)
CORS(app)


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(os.path.join("uploads", secure_filename(f.filename)))
    return 'file uploaded successfully'

@app.route('/images/', methods=['GET'])
def get_images():
    images_list = glob.glob(f"uploads/*")
    return send_file(os.path.join("predictions", "f10.png"), mimetype='image/png')
    # return str(images_list)


@app.route('/analysedImage/<name>', methods=['GET'])
def get_analysed_image(name):
    return send_file(os.path.join("predictions", name), mimetype='image/png')


@app.route('/analysedField/<name>/<count>', methods=['GET'])
def get_analysed_field(name, count):
    classification_test_model.analyse_image(name)
    print(name)
    return send_file(os.path.join("output", name + ".png"), mimetype='image/png')


@app.route('/getJsonClassification/<name>', methods=['GET'])
def get_json_colors(name):
    #array = classification_test_model.analyse_image(name)
    print("!!!")



@app.route('/polygons/<name>', methods=['GET'])
def get_polygons_analysed_image(name):
    f = open(f"predictions/{name}.json", "r")
    return f.read()

@app.route('/crop_image/<name>/<color>/<count>', methods=['GET'])
def crop_image(name, color, count):
    print(name)
    print(color)
    print(count)
    utils_draw_polygons.create_image_for_classification(name, color, count)
    return {}

@app.route('/analyse_image', methods=['POST'])
def analyse_image():
    f = request.files['file']
    f.save(os.path.join("uploads", secure_filename(f.filename)))
    test_model.analyse_image(f.filename)

    return send_file(os.path.join("predictions", f.filename), mimetype='image/png')


@app.route('/get_lat_long/<geodata>', methods=['GET'])
def get_lat_long(geodata):
    print(geodata)
    lat_long = geo_coding.getLatLong(geodata)

    return lat_long


@app.route('/json_classification/<name>', methods=['GET'])
def json_classification(name):
    print("#############")
    print(name)
    classification = classification_test_model.analyse_image(name)
    classOne = str(classification[0,0]) + ";" + str(classification[0,1]) + ";"+str(classification[0,2])

    return jsonify(classOne)


if __name__ == '__main__':
    app.run(host='0.0.0.0')