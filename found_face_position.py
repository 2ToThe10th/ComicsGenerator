import dataclasses
from typing import Union

import numpy as np

import cv2


@dataclasses.dataclass
class FacePosition:
    """
    (x, y) - top-left face bounding box coordinate
    """

    x: int
    y: int
    width: int
    height: int


def found_face_position(image: np.ndarray) -> Union[FacePosition, None]:
    """Generating the bounding box of the detected face in the image"""
    faceCascade = cv2.CascadeClassifier("face.xml")
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray_img,
        scaleFactor=1.05,
        minNeighbors=16,
        minSize=(100, 100),
    )

    if len(faces) == 0:
        print(f"Face not found")
        return None
    else:
        x, y, w, h = faces[0]
        print(f"Found face at {faces[0]}")
        return FacePosition(x=x, y=y, width=w, height=h)