import os
import time
from multiprocessing import Process


def worker():
    time.sleep(7)


def run_paint():
    proc = Process(target=worker, args=())
    proc.daemon = True
    proc.start()
    return proc