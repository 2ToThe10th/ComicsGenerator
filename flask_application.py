import io

import cv2
from flask import Flask, request, send_file
from flask_cors import CORS

from main import generate_comics

app = Flask("comics_app")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/generate_comics/', methods=["GET"])
def get_comics():
    comics_topic = request.args.get("comics_topic")
    print(f"get comics topic: {comics_topic}")
    comics_image = generate_comics(comics_topic, 6)
    _, comics_image_in_buffer = cv2.imencode(".jpg", comics_image)

    return send_file(io.BytesIO(comics_image_in_buffer), download_name="comics.jpg")
