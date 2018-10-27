import cv2
import numpy as np

from data import *
from bisect import bisect_left, bisect_right


def wells(image: np.ndarray, geo: Geo) -> None:
    image[:, geo.left_well_indent] = [255 * x for x in geo.left_well.core]
    image[:, geo.right_well_indent] = [255 * x for x in geo.right_well.core]


def lines(image: np.ndarray, geo: Geo, match: Match):
    for l1, l2, r1, r2 in match.iterator():
        cv2.line(image, (geo.left_well_indent, avg(l1, l2)), (geo.right_well_indent, avg(r1, r2)), 125, 1)


def fill(image: np.ndarray, geo: Geo, match: Match) -> None:

    _lines = [Line(l1, l2, r1, r2, geo) for l1, l2, r1, r2 in match.iterator()]

    for i in range(geo.width):
        # key_values = [(j, value) for (j, value) in _lines]
        # key_values.sort(key=lambda x: x[0])

        # up_value = None
        # down_value = key_values[0]

        for line in _lines:
            (j, value) = line(i)
            image[j, i] = 255 * max(0, min(1, value))


class Line:
    def __init__(self, left_from: int, left_to: int, right_from: int, right_to: int, geo: Geo):
        x1 = geo.left_well_indent
        y1 = avg(left_from, left_to)
        x2 = geo.right_well_indent
        y2 = avg(right_from, right_to)

        value1 = sum(geo.left_well.core[left_from: left_to]) / (left_to - left_from)
        value2 = sum(geo.right_well.core[right_from: right_to]) / (right_to - right_from)

        self.a = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.a * x1
        self.valueA = (value2 - value1) / (x2 - x1)
        self.valueB = value1 - self.valueA * x1

    def __call__(self, x) -> (int, float):
        return int(self.a * x + self.b), self.valueA * x + self.valueB


def avg(x1, x2) -> int:
    return (x2 - x1) // 2 + x1
