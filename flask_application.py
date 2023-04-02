import io

import cv2
from flask import Flask, request, send_file
from flask_cors import CORS

from generate_comics import generate_comics

app = Flask("comics_app")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/generate_comics/', methods=["GET"])
def generate_comics_endpoint():
    """Generate comics api endpoint"""
    comics_topic = request.args["comics_topic"]
    image_style = request.args["image_style"]
    width_images = int(request.args["width_images"])
    height_images = int(request.args["height_images"])
    print(f"get comics query: comics_topic: {comics_topic}, image_style: {image_style}, width_images: {width_images}, height_images: {height_images}")
    comics_image = generate_comics(comics_topic, image_style, width_images, height_images)

    _, comics_image_in_buffer = cv2.imencode(".jpg", comics_image)

    return send_file(io.BytesIO(comics_image_in_buffer), download_name="comics.jpg")
