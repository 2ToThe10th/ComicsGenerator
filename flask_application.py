import io

import cv2
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from gpt_panels import generate_comics
from main import get_next_comics_panel

app = Flask("comics_app")
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/get_comics/', methods=["GET"])
def get_comics():
    comics_topic = request.args.get("comics_topic")
    print(f"get comics topic: {comics_topic}")
    comics = generate_comics(comics_topic, 6)
    print(comics)
    return jsonify(comics)


@app.route('/get_panel/', methods=["GET"])
def get_picture():
    panel = request.args.get("panel")
    phrase = request.args.get("phrase")

    print(f'get query: panel="{panel}", phrase:"{phrase}')

    image = get_next_comics_panel(panel, phrase)
    _, im_buf_arr = cv2.imencode(".jpg", image)

    return send_file(io.BytesIO(im_buf_arr), download_name="panel.jpg")
