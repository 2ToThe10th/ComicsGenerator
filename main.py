import json
import urllib.request

import cv2
import openai
import numpy as np

from add_prompt_to_picture import add_prompt_to_picture
from found_face_position import found_face_position, FacePosition
from gpt_panels import generate_comics


def get_next_comics_panel(panel_situation: str, phrase: str) -> np.ndarray:
    print(f"get_next_comics_panel on situation: \"{panel_situation}\" and phrase: \"{phrase}\"")
    image = get_image_by_situation(panel_situation, style="cyberpunk")
    print("Got image from ChatGPT")
    find_face_try = 0
    if phrase is not None:
        face_position = found_face_position(image)
        while face_position is None:
            if find_face_try > 1:
                face_position = FacePosition(x=30, y=460, width=20, height=20)
                break
            print("Face not found, try again")
            image = get_image_by_situation(panel_situation, style="cyberpunk")
            print("Got image from ChatGPT")
            face_position = found_face_position(image)
            find_face_try += 1

        cv2.rectangle(
            image, (face_position.x, face_position.y), (face_position.x + face_position.width, face_position.y + face_position.height), (255, 255, 0), 2
        )
        add_prompt_to_picture(image, face_position, phrase)
    return image


def get_image_by_situation(situation_description: str, style: str) -> np.ndarray:
    result = openai.Image.create(prompt=f"Make photo in {style} style: {situation_description}", n=1, size="512x512")
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
    comics = generate_comics("an IT company which supports people with disabilities", 6)
    for index, v in enumerate(comics):
        panel = v["panel"]
        phrase = v["phrase"]
        image = get_next_comics_panel(panel, phrase)
        cv2.imwrite(f"out{index}.png", image)
        print(f"{index} image generated")


if __name__ == '__main__':
    main()
