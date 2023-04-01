import json
import urllib.request

import cv2
import openai
import numpy as np

from add_prompt_to_picture import add_prompt_to_picture
from found_face_position import found_face_position


def get_next_comics_panel(panel_situation: str, phrase: str) -> np.ndarray:
    image = get_image_by_situation(panel_situation, style="cyberpunk")
    print(type(image))
    face_position = found_face_position(image)
    add_prompt_to_picture(image, face_position, phrase)


def get_image_by_situation(situation_description: str, style: str) -> np.ndarray:
    result = openai.Image.create(prompt=f"Make photo in {style} style: {situation_description}", n=1, size="1024x1024")
    print(result)
    if "error" in result:
        raise ValueError(f"Error happened: {json.dumps(result['error'])}")
    if "data" not in result:
        raise ValueError(f"No data found: {json.dumps(result)}")
    image_request = urllib.request.urlopen(result["data"][0]["url"])
    image_in_array = np.asarray(bytearray(image_request.read()), dtype=np.uint8)
    return cv2.imdecode(image_in_array, -1)  # 'Load it as it is'



def main():
    # TODO: get panels from chatgpt
    image = get_next_comics_panel(
        "The man walks into a T-Mobile store, where he is greeted by a friendly sales representative.", "Welcome to T-Mobile! How can I assist you today?"
    )
    cv2.imwrite("out.png", image)


if __name__ == '__main__':
    main()
