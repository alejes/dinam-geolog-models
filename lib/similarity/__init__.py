from data.types import *


class Similarity:
    def __init__(self, border):
        self.__border = border

    def calculate(self, rock_a: RockTypes, rock_b: RockTypes, porosity_a: Porosity, porosity_b: Porosity) -> List[Line]:
        return [((1, 2), (2, 4))]
