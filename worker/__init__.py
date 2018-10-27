import os
import json
import time
import xlrd
from multiprocessing import Process


def load_excel(path):
    if not path:
        return []

    rb = xlrd.open_workbook(path)
    sheet = rb.sheet_by_index(0)
    ans=[]
    for rownum in range(sheet.nrows):
        ans.append(sheet.row_values(rownum))
    return ans


def worker(config):
    config = json.loads(config)
    print(config)
    print(config.values())
    rockA = load_excel(config.get('rock_A', None))
    rockB = load_excel(config.get('rock_B', None))
    porisityA = load_excel(config.get('porisity_A', None))
    porisityB = load_excel(config.get('porisity_B', None))
    print('rockA',rockA[:10])
    print('rockB', rockB[:10])
    print('porA', porisityA[:10])
    print('porB', porisityB[:10])
    time.sleep(7)


def run_paint(config):
    proc = Process(target=worker, args=[json.dumps(config)])
    proc.daemon = True
    proc.start()
    return proc