import cv2
import numpy as np
import json
import os
import statistics
import time

import xlrd
from multiprocessing import Process, Queue

from find_trapeziums import find_trapeziums
from painter.data import Geo, Match, Well, GeoTransformation
from painter import image
from painter import paint,seismic


class WorkerConfig:
    MAX_HIGN_SIZE = 600
    q = Queue()

def load_excel(path):
    if not path:
        return []

    rb = xlrd.open_workbook(path)
    sheet = rb.sheet_by_index(0)
    ans=[]
    for rownum in range(sheet.nrows):
        ans.append(sheet.row_values(rownum))
    return ans


def normalize_one(data, start, end, step):
    if not data:
        return []

    current = start
    index = 0
    values = []
    answer = []
    while current < end:
        if index < len(data) and current + step >= data[index][0]:
            # print (current + step, "<=", data[index][0])
            values.append(data[index][1])
            index += 1
        else:
            if not values:
                if index == 0:
                    values.append(data[0][1])
                elif index == len(data):
                    values.append(data[-1][1])
                else:
                    values.append(data[index][1])
            answer.append(statistics.median(values))
            values = []
            if index < len(data) and current + step == data[index][0]:
                values.append(data[index][1])
            current += step
    return answer


def encode_array(data):
    for el in data:
        if el[1] == 'sandstone':
            el[1] = 0
        else:
            el[1] = 1
    return data


def normalize_rocks(data1, data2, data3, data4):
    start = min(data1[0][0], data2[0][0], data3[0][0], data4[0][0])
    end = max(data1[-1][0], data2[-1][0], data3[0][0], data4[0][0])
    step = (end - start) / WorkerConfig.MAX_HIGN_SIZE
    print(start, end)
    print(step)
    n1 = normalize_one(data1, start, end, step)
    n2 = normalize_one(data2, start, end, step)
    n3 = normalize_one(data3, start, end, step)
    n4 = normalize_one(data4, start, end, step)
    return n1, n2, n3, n4, start, end, step


def worker(config, q):
    config = json.loads(config)
    print('put')

    print(config)
    print(config.values())
    _seismic = image.load(config.get("image_grid", "painter/SeismicScaled.jpg"))
    _transformation = seismic.parse_transformation(_seismic, 15 * 1000, int(2.5 * 1000), 2.5)
    rockA = load_excel(config.get('rock_A', "./sample_data/WellACoreDescription.xlsx"))
    rockB = load_excel(config.get('rock_B', "./sample_data/WellBCoreDescription.xlsx"))
    porisityA = load_excel(config.get('porisity_A', "./sample_data/WellA.xlsx"))
    porisityB = load_excel(config.get('porisity_B',  "./sample_data/WellB.xlsx"))
    rockA = encode_array(rockA)
    rockB = encode_array(rockB)
    print('rockA',rockA[:10])
    print('rockB', rockB[:10])
    print('porA', porisityA[:10])
    print('porB', porisityB[:10])

    nRockA, nRockB, nPorA, nPorB, start, end, step = normalize_rocks(rockA, rockB, porisityA, porisityB)
    print(nRockA[:10])
    print(nRockB[:10])
    print(nPorA[:10])
    print(nPorB[:10])
    print(start, end, step)
    global_min = round(min(list(map(lambda x: x[1], porisityA)) + list(map(lambda x: x[1], porisityB))), 2)
    global_max = round(max(list(map(lambda x: x[1], porisityA)) + list(map(lambda x: x[1], porisityB))), 2)
    print(global_min, global_max)

    print(len(nRockA), len(nRockB), len(nPorA), len(nPorB))
    res = find_trapeziums(nRockA, nRockB, nPorA, nPorB)
    print(res)

    _geo = Geo(
        Well(nRockA, nPorA),
        Well(nRockB, nPorB),
        _transformation.width,
        _transformation.left_well_intent,
        _transformation.right_well_intent
    )

    _match = Match(
        [match[1][0] for match in reversed(res)],
        [match[0][0] + 1 for match in reversed(res)],
        [match[1][1] for match in reversed(res)],
        [match[0][1] + 1 for match in reversed(res)],
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

    paint.save(add_scale(paint.depth(paint.resized(_core_result)), global_min, global_max), "core_4.png")
    paint.save(add_scale(paint.depth(paint.resized(_por_result)), global_min, global_max), "porosity_4.png")
    q.put({'rock-resized': paint.resized(_core_result),
           'data2': np.array(np.random.random((400, 500)) * 255, dtype=int)})


def run_paint(config):
    proc = Process(target=worker, args=[json.dumps(config), WorkerConfig.q])
    proc.daemon = True
    proc.start()
    return proc