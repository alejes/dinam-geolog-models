import os
import json
import time
from multiprocessing import Process


def worker(config):
    config = json.loads(config)
    print(config)
    print(config.values())
    time.sleep(7)


def run_paint(config):
    proc = Process(target=worker, args=[json.dumps(config)])
    proc.daemon = True
    proc.start()
    return proc