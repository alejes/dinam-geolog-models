import cv2

import image
import paint
from data import *

if __name__ == '__main__':
    _geo = Geo(Well.generate_left(), Well.generate_right(), 1000, 250, 750)
    _match = Match.generate()
    _image = image.create(_geo.height, _geo.width)

    paint.wells(_image, _geo)
    # paint.lines(_image, _geo, _match)
    paint.fill(_image, _geo, _match)

    image.show(_image)
