import dataclasses

import numpy as np


@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass
class FacePosition:
    top_left: Point
    bottom_right: Point


def found_face_position(image: np.ndarray) -> FacePosition:
    pass  # TODO(Slava Pirat): find face
