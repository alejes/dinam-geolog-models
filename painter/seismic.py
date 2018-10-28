import cv2
import numpy as np

from data import *


def parse_transformation(image: np.ndarray, width_m: int, left_height: int, k: float) -> GeoTransformation:

    layers = []

    def find_layer(index):
        orange_end = None
        yellow_start = None
        contains_well = False
        for j in range(image.shape[0]):
            b, g, r = image[j, index, :]

            if r > 200 > g > 100 > b:  # maybe orange
                orange_end = j
            elif r > 200 and g > 200 and 100 > b:  # maybe yellow
                yellow_start = j
            elif r < 100 and g < 100 and b > 110:  # maybe blue
                contains_well = True

            if orange_end is not None and yellow_start is not None:
                return Layer(orange_end, yellow_start, contains_well)

            if r > 180 > g > 100 > b:  # maybe maybe orange
                orange_end = j

        return None

    for i in range(image.shape[1]):

        layer = find_layer(i)

        if layer is not None:
            layers.append(layer)

    for index, layer in enumerate(layers):
        if layer.to_depth - layer.from_depth < 10:
            layer.from_depth = (layers[index - 2].from_depth + layers[index + 2].from_depth) // 2

    width_k = width_m / len(layers) / k
    height_k = left_height / (layers[0].to_depth - layers[0].from_depth) / k
    min_depth = min(layer.from_depth for layer in layers)

    def adopt(depth):
        return int((depth - min_depth) * height_k)

    # new_width = int(width_m / k)
    new_width = len(layers) * int(width_k)  # width_k ~= 5.016
    new_height = int((max(layer.to_depth for layer in layers) - min_depth) * height_k)
    new_layers = [l for layer in layers for l
                  in [Layer(adopt(layer.from_depth), adopt(layer.to_depth), layer.contains_well)] * int(width_k)]

    left_well_intent = min(i for i, layer in enumerate(new_layers) if layer.contains_well)
    right_well_intent = max(i for i, layer in enumerate(new_layers) if layer.contains_well)

    return GeoTransformation(new_layers, new_width, new_height, left_well_intent, right_well_intent)


def paint_transformation(image: np.ndarray, transformation: GeoTransformation, source: np.ndarray):
    assert image.shape[0] == transformation.height
    assert image.shape[1] == transformation.width
    assert source.shape[1] == transformation.width

    for i, layer in enumerate(transformation.layers):
        image[layer.from_depth: layer.to_depth, i] = \
            cv2.resize(np.asmatrix(source[:, i]), (layer.to_depth - layer.from_depth, 1))

