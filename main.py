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
    if phrase is not None:
        face_position = found_face_position(image)
        add_prompt_to_picture(image, face_position, phrase)
    return image


def get_image_by_situation(situation_description: str, style: str) -> np.ndarray:
    return cv2.imread("img.png")
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
        "A man with messy hair and glasses is seen walking on the street while staring at his old and outdated phone. He looks frustrated and annoyed.",
        "Ugh, this phone is driving me crazy. I need a new one",
    )
    cv2.imwrite("out.png", image)


if __name__ == '__main__':
    main()
