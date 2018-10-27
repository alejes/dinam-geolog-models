import cv2

import image
import paint
import seismic
from data import *

if __name__ == '__main__':
    _seismic = image.load("SeismicScaled.jpg")
    _transformation = seismic.parse_transformation(_seismic, 15 * 1000, int(2.5 * 1000), 10)

    _geo = Geo(Well.generate_left(), Well.generate_right(), _transformation.width, _transformation.left_well_intent, _transformation.right_well_intent)
    _match = Match.generate()
    _image = image.create(_geo.height, _geo.width)

    # image.show(_seismic)

    paint.wells(_image, _geo)
    paint.lines(_image, _geo, _match)
    paint.fill(_image, _geo, _match)

    # _image1 = _image.copy()
    # paint.fill(_image1, _geo, _match)
    # paint.wells(_image1, _geo)
    #
    # _, _image2 = cv2.threshold(_image1, 127, 255, cv2.THRESH_BINARY)
    #
    # print("Showing ...")
    # image.show(_image, _image1, _image2)

    _result = image.create(_transformation.height, _transformation.width)
    seismic.paint_transformation(_result, _transformation, _image)

    image.show(_image, _result)
