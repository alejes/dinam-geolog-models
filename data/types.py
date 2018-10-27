from enum import Enum
from typing import List, AnyStr, Tuple, NamedTuple

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

FilePath = AnyStr

class Lithofacies(Enum):
    Sandstone=1
    Shale=2


WellData = NamedTuple('WellData', [('RockType', Lithofacies), ('Porosity', float)])
TaskConfig = NamedTuple('TaskConfig', [('ImageGrid', FilePath), ('WellA', WellData), ('WellB', WellData)])
