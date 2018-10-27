from typing import List, Tuple, NamedTuple

Point = NamedTuple('Point', [('x', float), ('y', float)])
Color = NamedTuple('Color', [('r', int), ('g', int), ('b', int)])
ColorPoint = NamedTuple('ColorPoint', [('point', Point), ('color', Color)])
Bitmap = List[List[ColorPoint]]

Interval = NamedTuple('Interval', [('a', int), ('b', int)])
Line = NamedTuple('Line', [('a', Interval), ('b', Interval)])

Porosity = List[float]
RockTypes = List[float]

ContourLine = List[Point]
Well = Point
