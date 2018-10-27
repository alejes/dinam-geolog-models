from typing import List, Tuple

Point = Tuple[float, float]
Color = Tuple[int, int, int]
ColorPoint = Tuple[Point, Color]
Bitmap = List[List[ColorPoint]]

Interval = Tuple[int, int]
Line = Tuple[Interval, Interval]

Porosity = List[float]
RockTypes = List[float]

ContourLine = List[Point]
Well = Point
