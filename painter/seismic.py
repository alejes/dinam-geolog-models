import numpy as np

from data import *


def parse_transformation(image: np.ndarray, width_m: int, left_height: int) -> GeoTransformation:

    k = 5  # TODO 2.5

    layers = []
    head_layer = None
    last_layer = None

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
            if head_layer is None:
                head_layer = i
            last_layer = i

    for index, layer in enumerate(layers):
        if layer.to_depth - layer.from_depth < 10:
            layer.from_depth = (layers[index - 2].from_depth + layers[index + 2].from_depth) // 2

    # for layer in layers:
    #     print(layer.from_depth, layer.to_depth, layer.contains_well)

    width_k = width_m / (last_layer - head_layer) / k
    height_k = left_height / (layers[0].to_depth - layers[0].from_depth) / k
    min_depth = min(layer.from_depth for layer in layers)

    print(width_k, len(layers))

    def adopt(depth):
        return int((depth - min_depth) * height_k)

    # new_width = int(width_m / k) + 1
    new_width = len(layers)
    new_height = int((max(layer.to_depth for layer in layers) - min_depth) * height_k) + 1
    new_layers = [Layer(adopt(layer.from_depth), adopt(layer.to_depth), layer.contains_well) for layer in layers]
    # final_layers = [Layer() for layer in layers]

    return GeoTransformation(new_layers, new_width, new_height)


def paint_transformation(image: np.ndarray, transformation: GeoTransformation):
    assert image.shape[0] == transformation.height
    assert image.shape[1] == transformation.width

    for i, layer in enumerate(transformation.layers):
        image[layer.from_depth, i] = 255
        image[layer.to_depth, i] = 255

