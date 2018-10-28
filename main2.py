import painter.image as image
import painter.paint as paint
import painter.seismic as seismic
from find_trapeziums import find_trapeziums
from painter.data import *
from worker import load_excel, encode_array, normalize_rocks
import numpy as np
import cv2


data = image.load("porosity.png")
scale = image.load("scale/colorscale_jet.jpg")

# data[data.shape[0]-20-scale.shape[0]:data.shape[0], data.shape[1]-20-scale.shape[1]:data.shape[1]] = np.zeros((20+scale.shape[0], 20+scale.shape[1],3))
# data[data.shape[0]-10-scale.shape[0]:data.shape[0]-10, data.shape[1]-10-scale.shape[1]:data.shape[1]-10] = scale
# # data[20:20+scale.shape[0], 10:10+scale.shape[1]] = scale
# data = cv2.putText(data, "0.04", (data.shape[0]-scale.shape[0]+5,data.shape[1]-15-scale.shape[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
# data = cv2.putText(data, "4.44", (data.shape[1]-50,data.shape[1]-15-scale.shape[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
#
#
# image.show(data)

def add_scale(data, min, max):
    scale = image.load("scale/colorscale_jet.jpg")
    data[data.shape[0] - 20 - scale.shape[0]:data.shape[0],
    data.shape[1] - 20 - scale.shape[1]:data.shape[1]] = np.zeros((20 + scale.shape[0], 20 + scale.shape[1], 3))
    data[data.shape[0] - 10 - scale.shape[0]:data.shape[0] - 10,
    data.shape[1] - 10 - scale.shape[1]:data.shape[1] - 10] = scale
    # data[20:20+scale.shape[0], 10:10+scale.shape[1]] = scale
    # print(data.shape[0] - scale.shape[0] + 5, data.shape[1] - 15 - scale.shape[1])
    data = cv2.putText(data, str(min), (data.shape[0] - scale.shape[0] + 5, data.shape[1] - 15 - scale.shape[1]),
                       cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    data = cv2.putText(data, str(max), (data.shape[1] - 50, data.shape[1] - 15 - scale.shape[1]),
                       cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    return data

global_min = 0.004
global_max = 4.004

image.show(add_scale(data, global_min, global_max))