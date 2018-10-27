from abc import ABC
from typing import List, Sized


class Well(Sized, ABC):
    def __init__(self, core: List[float], log: List[float]) -> None:
        assert len(core) == len(log)
        self.core = core
        self.log = log

    def __len__(self):
        return len(self.core)

    @staticmethod
    def generate_left() -> 'Well':
        core = [1.0] * 100 + [0.1] * 200 + [0.7] * 50 + [0.0] * 100 + [1.0] * 50
        return Well(core, core.copy())

    @staticmethod
    def generate_right() -> 'Well':
        core = [0.7] * 50 + [0.0] * 100 + [1.0] * 50 + [0.1] * 200 + [0.7] * 40 + [0] * 20 + [0.7] * 40
        return Well(core, core.copy())


class Geo:
    def __init__(self, left_well: Well, right_well: Well, width: int, left_well_indent: int, right_well_indent: int) -> None:
        assert len(left_well) == len(right_well)
        assert left_well_indent > 0
        assert left_well_indent < right_well_indent
        assert right_well_indent < width
        self.left_well = left_well
        self.right_well = right_well
        self.width = width
        self.left_well_indent = left_well_indent
        self.right_well_indent = right_well_indent

    @property
    def height(self) -> int:
        return len(self.right_well.core)


class Layer:
    def __init__(self, from_depth: int, to_depth: int, contains_well: bool) -> None:
        self.from_depth = from_depth
        self.to_depth = to_depth
        self.contains_well = contains_well


class GeoTransformation:
    def __init__(self, layers: List[Layer], width: int, height: int, left_well_intent: int, right_well_intent: int) -> None:
        self.layers = layers
        self.width = width
        self.height = height
        self.left_well_intent = left_well_intent
        self.right_well_intent = right_well_intent


class Match:
    def __init__(self, left_from: List[int], left_to: List[int], right_from: List[int], right_to: List[int]) -> None:
        assert len(left_from) == len(left_to)
        assert len(left_to) == len(right_from)
        assert len(right_from) == len(right_to)
        self.left_from = left_from
        self.left_to = left_to
        self.right_from = right_from
        self.right_to = right_to

    def iterator(self):
        return zip(self.left_from, self.left_to, self.right_from, self.right_to)

    @staticmethod
    def generate() -> 'Match':
        left_from   = [  0, 100, 300, 350, 450, 475]
        left_to     = [100, 300, 350, 450, 475, 500]
        right_from  = [  0,  50, 150, 200, 400, 460]
        right_to    = [ 50, 150, 200, 400, 440, 500]
        return Match(left_from, left_to, right_from, right_to)

