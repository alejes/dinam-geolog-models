import cv2

import image
import paint
from data import *

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from find_trapeziums import test_trapeziums

if __name__ == '__main__':
    # _geo = Geo(Well.generate_left(), Well.generate_right(), 1000, 250, 750)
    # _match = Match.generate()

    #test shit begin
    test_data, test_match = test_trapeziums()
    _geo = Geo(
        Well(test_data[0], test_data[2]), 
        Well(test_data[1], test_data[3]), 
        1000, 
        250,
        750
    )
    _match = Match(
        [match[0][0] for match in test_match],
        [match[1][0] for match in test_match],
        [match[0][1] for match in test_match],
        [match[1][1] for match in test_match],
    )
    #test shit end
    _image = image.create(_geo.height, _geo.width)

    paint.wells(_image, _geo)
    paint.lines(_image, _geo, _match)
    # paint.fill(_image, _geo, _match)

    image.show(_image)
