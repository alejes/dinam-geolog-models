import json
import os
import statistics
import time

import xlrd
from multiprocessing import Process

from find_trapeziums import find_trapeziums
from painter.data import Geo, Match, Well
from painter import image
from painter import paint


class WorkerConfig:
    MAX_HIGN_SIZE = 600

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


def worker(config):
    config = json.loads(config)
    print(config)
    print(config.values())
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

    print(len(nRockA), len(nRockB), len(nPorA), len(nPorB))
    res = find_trapeziums(nRockA, nRockB, nPorA, nPorB)
    print(res)

    _geo = Geo(
        Well(nRockA, nPorA),
        Well(nRockB, nRockB),
        1000,
        250,
        750
    )

    _match = Match(
        [match[0][0] for match in res],
        [match[1][0] for match in res],
        [match[0][1] for match in res],
        [match[1][1] for match in res],
    )

    _image = image.create(_geo.height, _geo.width)

    paint.wells(_image, _geo)
    paint.lines(_image, _geo, _match)
    # paint.fill(_image, _geo, _match)

    image.show(_image)

    time.sleep(7)


def run_paint(config):
    proc = Process(target=worker, args=[json.dumps(config)])
    proc.daemon = True
    proc.start()
    return proc