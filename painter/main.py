import cv2

import image
import paint
import seismic
from data import *

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from find_trapeziums import test_trapeziums

if __name__ == '__main__':
    # _geo = Geo(Well.generate_left(), Well.generate_right(), 1000, 250, 750)
    # _match = Match.generate()

    _seismic = image.load("painter/SeismicScaled.jpg")
    _transformation = seismic.parse_transformation(_seismic, 15 * 1000, int(2.5 * 1000), 10)  # 2.5

    #test shit begin
    test_data, test_match = test_trapeziums()
    _geo = Geo(
        Well(test_data[0], test_data[2]), 
        Well(test_data[1], test_data[3]), 
        _transformation.width,
        _transformation.left_well_intent,
        _transformation.right_well_intent
    )
    _match = Match(
        [match[1][0] for match in reversed(test_match)],
        [match[0][0] + 1 for match in reversed(test_match)],
        [match[1][1] for match in reversed(test_match)],
        [match[0][1] + 1 for match in reversed(test_match)],
    )
    #test shit end
    _image = image.create(_geo.height, _geo.width)

    # paint.lines(_image, _geo, _match)
    paint.fill(_image, _geo, _match)
    paint.wells(_image, _geo)

    _base_image = image.create(_geo.height, _geo.width)
    paint.wells(_base_image, _geo)
    paint.lines(_base_image, _geo, _match)

    _result = image.create(_transformation.height, _transformation.width)
    seismic.paint_transformation(_result, _transformation, _image)

    image.show(_image, _base_image, _result, paint.bined(_result))
