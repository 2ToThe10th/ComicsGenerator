import cv2
import numpy as np

from found_face_position import FacePosition


def rounded_rectangle(
    image,
    top_left,
    bottom_right,
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

    p1 = top_left
    p2 = (bottom_right[0], top_left[1])
    p3 = bottom_right
    p4 = (top_left[0], bottom_right[1])

    # draw fillings
    cv2.rectangle(image, (top_left[0], top_left[1] + radius), (bottom_right[0], bottom_right[1] - radius), fill_color, -1)
    cv2.rectangle(image, (top_left[0] - radius, top_left[1]), (bottom_right[0] + radius, bottom_right[1]), fill_color, -1)
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


def find_place_for_phrase():
    return (50, 50)


def add_prompt_to_picture(image: np.ndarray, face_position: FacePosition, phrase: str) -> None:
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = find_place_for_phrase()
    thickness = 1
    font_scale = 0.5

    x = cv2.getTextSize(phrase, fontScale=font_scale, fontFace=font, thickness=thickness)
    print(x)

    image = rounded_rectangle(image, org, (org[0] + x[0][0], org[1] - x[0][1]), radius=20, thickness=2)
    image = cv2.putText(image, phrase, org, font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
