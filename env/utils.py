import time
import logging


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

