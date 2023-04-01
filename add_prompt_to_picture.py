import dataclasses
from typing import Union

import cv2
import numpy as np

from found_face_position import FacePosition

FONT = cv2.FONT_HERSHEY_DUPLEX
LINE_GAP = 6


@dataclasses.dataclass
class TextPosition:
    top: int
    bottom: int
    left: int
    right: int
    font_scale: float


def rounded_rectangle(
    image,
    phrase_place: TextPosition,
    radius,
    fill_color=(255, 255, 255),
    line_color=(0, 0, 0),
    thickness=1,
    line_type=cv2.LINE_AA,
):
    #  corners:
    #  p1(top_left) - p2
    #  |     |
    #  p4 - p3(bottom_right)

    p1 = (phrase_place.left, phrase_place.bottom)
    p2 = (phrase_place.right, phrase_place.bottom)
    p3 = (phrase_place.right, phrase_place.top)
    p4 = (phrase_place.left, phrase_place.top)

    # draw fillings
    print((phrase_place.left, phrase_place.bottom + radius), (phrase_place.right, phrase_place.top - radius), fill_color, -1)
    cv2.rectangle(image, (phrase_place.left, phrase_place.bottom + radius), (phrase_place.right, phrase_place.top - radius), fill_color, -1)
    cv2.rectangle(image, (phrase_place.left - radius, phrase_place.bottom), (phrase_place.right + radius, phrase_place.top), fill_color, -1)
    # draw straight lines
    for p_start, p_end, direction_shift_right, direction_shift_top in [(p1, p2, 0, 1), (p2, p3, 1, 0), (p3, p4, 0, -1), (p4, p1, -1, 0)]:
        cv2.line(
            image,
            (p_start[0] + direction_shift_right * radius, p_start[1] + direction_shift_top * radius),
            (p_end[0] + direction_shift_right * radius, p_end[1] + direction_shift_top * radius),
            line_color,
            thickness,
            line_type,
        )

    # draw arcs
    angle = 90
    for p in [p1, p2, p3, p4]:
        cv2.ellipse(image, p, (radius, radius), 0, angle, (angle + 90), fill_color, -1)
        cv2.ellipse(image, p, (radius, radius), 0, angle, (angle + 90), line_color, thickness)
        angle -= 90
        angle %= 360

    return image


def needed_height(split_phrase: list[str], width: int, font_scale: float, thickness: int) -> Union[int, None]:
    for word in split_phrase:
        if len(word) > width:
            return None

    height = 0
    words = []
    for word in split_phrase:
        words.append(word)
        line = ' '.join(words)
        (w, h), _ = cv2.getTextSize(line, fontScale=font_scale, fontFace=FONT, thickness=thickness)
        if w > width:
            words = words[-1:]
            height += h + int(LINE_GAP * font_scale)

    if words:
        (_, h), _ = cv2.getTextSize(' '.join(words), fontScale=font_scale, fontFace=FONT, thickness=thickness)
        height += h + int(LINE_GAP * font_scale)

    if height > 0:
        height -= int(LINE_GAP * font_scale)

    return height


def find_place_for_phrase(
    image: np.ndarray, face_position: FacePosition, split_phrase: list[str], thickness: int, corner_min_size=10, delta_on_width=10
) -> TextPosition:
    image_height, image_width, _ = image.shape
    place_at_left = face_position.x - 2 * corner_min_size
    place_at_right = image_width - face_position.x - face_position.width - 2 * corner_min_size
    maximum_exists_width = max(place_at_right, place_at_left)
    font_scale = 1
    while True:
        text_height = None
        new_text_width = maximum_exists_width + delta_on_width
        while True:
            new_text_height = needed_height(split_phrase, new_text_width - delta_on_width, font_scale, thickness)
            print(font_scale, new_text_height, new_text_width - delta_on_width)
            if (
                new_text_height is None
                or new_text_height > image_height - 2 * corner_min_size
                or (text_height is not None and new_text_height > (2.0 / 3.0 * (new_text_width - delta_on_width)))
            ):
                if text_height is None:
                    break
                else:
                    print(text_height)
                    print(new_text_width)
                    top = max(
                        corner_min_size, min(face_position.y + face_position.height // 2 - text_height // 2, image_height - corner_min_size - text_height)
                    )
                    if place_at_left >= place_at_right:
                        left = face_position.x - corner_min_size - new_text_width
                    else:
                        left = face_position.x + face_position.width + corner_min_size
                    right = left + new_text_width
                    ans = TextPosition(top=top, bottom=top + text_height, left=left, right=right, font_scale=font_scale)
                    print(ans)
                    return ans

            text_height = new_text_height
            new_text_width -= delta_on_width

        if font_scale < 0.25:
            break
        else:
            font_scale -= 0.5
            continue

    text_height = needed_height(split_phrase, image_width - 2 * corner_min_size, font_scale, thickness)
    if text_height < (image_height - face_position.y - face_position.height - corner_min_size):
        top = face_position.x + face_position.height + corner_min_size
        return TextPosition(top=top, bottom=top + text_height, left=corner_min_size, right=image_width - corner_min_size, font_scale=font_scale)
    else:
        return TextPosition(
            top=corner_min_size, bottom=corner_min_size + text_height, left=corner_min_size, right=image_width - corner_min_size, font_scale=font_scale
        )


def print_line(image: np.ndarray, line: str, left: int, top: int, width: int, font_scale: float, thickness: int):
    (w, h), _ = cv2.getTextSize(line, fontScale=font_scale, fontFace=FONT, thickness=thickness)
    cv2.putText(image, line, (left + (width - w) // 2, top + h), FONT, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)


def print_text_by_line(image: np.ndarray, split_phrase: list[str], thickness: int, text_position: TextPosition):
    width = text_position.right - text_position.left
    current_top = text_position.top
    words = []
    for word in split_phrase:
        words.append(word)
        line = ' '.join(words)
        (w, h), _ = cv2.getTextSize(line, fontScale=text_position.font_scale, fontFace=FONT, thickness=thickness)
        if w > width:
            line = ' '.join(words[:-1])
            print_line(image, line, text_position.left, current_top, width, text_position.font_scale, thickness)
            current_top += h + int(LINE_GAP * text_position.font_scale)
            words = words[-1:]

    if words:
        print_line(image, ' '.join(words), text_position.left, current_top, width, text_position.font_scale, thickness)


def add_prompt_to_picture(image: np.ndarray, face_position: FacePosition, phrase: str) -> None:
    split_phrase = phrase.split()
    thickness = 1
    phrase_place = find_place_for_phrase(image, face_position, split_phrase, thickness)

    print(f"Found place for phrase: {phrase_place}")

    rounded_rectangle(image, phrase_place, radius=5, thickness=2)
    print_text_by_line(image, split_phrase, thickness, phrase_place)
