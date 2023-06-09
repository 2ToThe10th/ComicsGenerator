import numpy as np
from typing import List

IMAGE_HEIGHT = 512
IMAGE_WIDTH = 512
PADDING = 20


def concatenate_images(images: List[np.ndarray], horizontal_num: int, vertical_num: int) -> np.ndarray:
    """Creating a comics from the given list of images"""
    number_of_images = horizontal_num * vertical_num
    assert len(images) == number_of_images

    final_width = IMAGE_WIDTH * horizontal_num + PADDING * (horizontal_num + 1)
    final_height = IMAGE_HEIGHT * vertical_num + PADDING * (vertical_num + 1)

    background = np.zeros((final_height, final_width, 3), np.uint8)

    counter = 0
    for v_pos in range(vertical_num):
        for h_pos in range(horizontal_num):
            x_coord = v_pos * IMAGE_WIDTH + PADDING * (v_pos + 1)
            y_coord = h_pos * IMAGE_WIDTH + PADDING * (h_pos + 1)

            background[x_coord : (x_coord + IMAGE_HEIGHT), y_coord : (y_coord + IMAGE_WIDTH)] = images[counter]
            counter += 1

    return background
