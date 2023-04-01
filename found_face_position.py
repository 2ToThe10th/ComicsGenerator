import dataclasses

import numpy as np

import cv2

@dataclasses.dataclass
class FacePosition:
    '''
    (x, y) - top-left face bounding box coordinate
    '''
    x: int
    y: int
    width: int
    height: int



def found_face_position(image: np.ndarray) -> FacePosition:
    faceCascade = cv2.CascadeClassifier("face.xml")
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray_img,
        scaleFactor=1.05,
        minNeighbors=16,
        minSize=(100, 100),
    )

    if faces == []:
        return None
    else:
        x, y, w, h = faces[0]
        print(faces[0])
        return FacePosition(x=x, y=y, width=w, height=h)
    return


