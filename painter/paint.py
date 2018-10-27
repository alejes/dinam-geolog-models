from itertools import groupby

import cv2
import numpy as np

from data import *
from painter.data import Geo, Match


def wells(image: np.ndarray, geo: Geo) -> None:
    image[:, geo.left_well_indent] = [255 * x for x in geo.left_well.core]
    image[:, geo.right_well_indent] = [255 * x for x in geo.right_well.core]


def lines(image: np.ndarray, geo: Geo, match: Match):
    for l1, l2, r1, r2 in match.iterator():
        cv2.line(image, (geo.left_well_indent, avg(l1, l2)), (geo.right_well_indent, avg(r1, r2)), 125, 1)


def fill(image: np.ndarray, geo: Geo, match: Match) -> None:

    _lines = [create_lines(l1, l2, r1, r2, geo) for l1, l2, r1, r2 in match.iterator()]

    for i in range(geo.width):
        key_values = [(x, np.mean([a[1] for a in group])) for (x, group)
                      in groupby(sorted(((int(line(i)), value_line(i))
                                         for (line, value_line) in _lines), key=lambda n: n[0]), key=lambda m: m[0])
                      if 0 <= x < geo.height]
        key_values.sort(key=lambda x: x[0])
        # print(key_values)

        up_index = None
        down_index = 0  # assume non empty

        for j in range(geo.height):

            if down_index is not None and j > key_values[down_index][0]:
                up_index = down_index
                down_index = down_index + 1 if down_index < len(key_values) - 1 else None

            if up_index is None:
                value = key_values[down_index][1]
            elif down_index is None:
                value = key_values[up_index][1]
            else:
                delta = key_values[down_index][0] - key_values[up_index][0]
                down = (j - key_values[up_index][0]) / delta
                up = (key_values[down_index][0] - j) / delta
                value = up * key_values[up_index][1] + down * key_values[down_index][1]

            image[j, i] = 255 * max(0, min(1, value))


class Line:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def __call__(self, x) -> float:
        return self.a * x + self.b


def create_lines(left_from: int, left_to: int, right_from: int, right_to: int, geo: Geo) -> (Line, Line):
    x1 = geo.left_well_indent
    y1 = avg(left_from, left_to)
    x2 = geo.right_well_indent
    y2 = avg(right_from, right_to)

    value1 = sum(geo.left_well.core[left_from: left_to]) / (left_to - left_from)
    value2 = sum(geo.right_well.core[right_from: right_to]) / (right_to - right_from)

    a = (y2 - y1) / (x2 - x1)

    value_a = (value2 - value1) / (x2 - x1)

    return Line(a, y1 - a * x1), Line(value_a, value1 - value_a * x1)


# def avg_line(line1: Line, line2: Line, x: int, y: int) -> Line:
#     a = line1.a + line2.a
#     return Line( )


def avg(x1, x2) -> int:
    if x1 > x2:
        return avg(x2, x1)
    return (x2 - x1) // 2 + x1
