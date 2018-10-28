import painter.image as image
import painter.paint as paint
import painter.seismic as seismic
from find_trapeziums import find_trapeziums, test_trapeziums
from painter.data import *
from worker import load_excel, encode_array, normalize_rocks

if __name__ == '__main__':

    _seismic = image.load("painter/SeismicScaled.jpg")
    _transformation = seismic.parse_transformation(_seismic, 15 * 1000, int(2.5 * 1000), 2.5)

    rockA = load_excel("./sample_data/WellACoreDescription.xlsx")
    rockB = load_excel("./sample_data/WellBCoreDescription.xlsx")
    porisityA = load_excel("./sample_data/WellA.xlsx")
    porisityB = load_excel("./sample_data/WellB.xlsx")
    rockA = encode_array(rockA)
    rockB = encode_array(rockB)

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

    _base_image = image.create(_geo.height, _geo.width)
    paint.wells(_base_image, _geo)
    paint.lines(_base_image, _geo, _match)

    _core = image.create(_geo.height, _geo.width)
    paint.fill(_core, _geo, _match, name="core")

    _por = image.create(_geo.height, _geo.width)
    paint.fill(_por, _geo, _match, name="log")

    _core_result = image.create(_transformation.height, _transformation.width)
    seismic.paint_transformation(_core_result, _transformation, paint.bined(paint.filtered(_core)))

    _por_result = image.create(_transformation.height, _transformation.width)
    seismic.paint_transformation(_por_result, _transformation, paint.filtered(_por))

    paint.save(_core_result, "core.png")
    paint.save(_por_result, "porosity.png")

    image.show(paint.resized(_core_result), paint.resized(_por_result))
