import painter.image as image
import painter.paint as paint
import painter.seismic as seismic
from find_trapeziums import find_trapeziums, test_trapeziums
from painter.data import *
from worker import load_excel, encode_array, normalize_rocks
import cv2
import numpy as np

if __name__ == '__main__':

    _seismic = image.load("painter/SeismicScaled.jpg")
    _transformation = seismic.parse_transformation(_seismic, 15 * 1000, int(2.5 * 1000), 2.5)

    rockA = load_excel("./sample_data/WellACoreDescription.xlsx")
    rockB = load_excel("./sample_data/WellBCoreDescription.xlsx")
    porisityA = load_excel("./sample_data/WellA.xlsx")
    porisityB = load_excel("./sample_data/WellB.xlsx")
    rockA = encode_array(rockA)
    rockB = encode_array(rockB)

    global_min = round(min(list(map(lambda x: x[1], porisityA)) + list(map(lambda x: x[1], porisityB))), 2)
    global_max = round(max(list(map(lambda x: x[1], porisityA)) + list(map(lambda x: x[1], porisityB))), 2)

    test_data, test_match = test_trapeziums()
    _geo = Geo(
        Well(test_data[0], test_data[2]),
        Well(test_data[1], test_data[3]),
        _transformation.width,
        _transformation.left_well_intent,
        _transformation.right_well_intent
    )

    # nRockA, nRockB, nPorA, nPorB, start, end, step = normalize_rocks(rockA, rockB, porisityA, porisityB)
    # test_match = find_trapeziums(nRockA, nRockB, nPorA, nPorB)
    # _geo = Geo(
    #     Well(nRockA, nPorA),
    #     Well(nRockB, nPorB),
    #     _transformation.width,
    #     _transformation.left_well_intent,
    #     _transformation.right_well_intent
    # )

    _match = Match(
        [match[1][0] for match in reversed(test_match)],
        [match[0][0] + 1 for match in reversed(test_match)],
        [match[1][1] for match in reversed(test_match)],
        [match[0][1] + 1 for match in reversed(test_match)],
    )

    _base_image = image.create(_geo.height, _geo.width, True)
    paint.wells(_base_image, _geo)
    paint.lines(_base_image, _geo, _match)

    _core = image.create(_geo.height, _geo.width, True)
    paint.fill(_core, _geo, _match, name="core")

    _por = image.create(_geo.height, _geo.width, True)
    paint.fill(_por, _geo, _match, name="log")

    _core_result = image.create(_transformation.height, _transformation.width, True)
    seismic.paint_transformation(_core_result, _transformation, paint.bined(paint.filtered(_core)))

    _por_result = image.create(_transformation.height, _transformation.width, True)
    seismic.paint_transformation(_por_result, _transformation, paint.filtered(_por))

    print(_core_result.shape)

    paint.save(paint.colorize(_core_result), "core.png")
    print(_core_result)
    paint.save(_por_result, "porosity.png")


    # image.show(paint.resized(_core_result), paint.resized(_por_result))


    def add_scale(data, min, max):
        scale = image.load("scale/colorscale_jet.jpg")
        data[data.shape[0] - 20 - scale.shape[0]:data.shape[0],
        data.shape[1] - 20 - scale.shape[1]:data.shape[1]] = np.zeros((20 + scale.shape[0], 20 + scale.shape[1], 3))
        data[data.shape[0] - 10 - scale.shape[0]:data.shape[0] - 10,
        data.shape[1] - 10 - scale.shape[1]:data.shape[1] - 10] = scale
        # data[20:20+scale.shape[0], 10:10+scale.shape[1]] = scale
        data = cv2.putText(data, str(min), (data.shape[0] - scale.shape[0] + 5, data.shape[1] - 15 - scale.shape[1]),
                           cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        data = cv2.putText(data, str(max), (data.shape[1] - 50, data.shape[1] - 15 - scale.shape[1]),
                           cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        return data


    res = paint.resized(_core_result)
    paint.save(paint.colorize(paint.resized(_core_result)), "core_2.png")
    print(res)

    paint.save(paint.depth(paint.resized(_por_result)), "porosity_2.png")

    paint.save(add_scale(paint.depth(_core_result), global_min, global_max), "core_3.png")
    paint.save(add_scale(paint.depth(_por_result), global_min, global_max), "porosity_3.png")

    paint.save(add_scale(paint.depth(paint.resized(_core_result)), global_min, global_max), "core_4.png")
    paint.save(add_scale(paint.depth(paint.resized(_por_result)), global_min, global_max), "porosity_4.png")