from timeit import default_timer as now
import os
from enum import Enum, unique

__all__ = ["VIDEO_EXT", "IMG_EXT", "FOURCC_CODEC", "FATAL_ERROR", "ERROR", "WARNING",
           "INFOMATION", "IGNORE", "colors", "report", "chronograph"]

VIDEO_EXT = ('.mp4', '.avi', '.mpg', '.mpeg', '.mov')
IMG_EXT = ('.jpg', '.jpeg', '.jpe', '.png', '.bmp', '.dib', '.tif', '.tiff')
FOURCC_CODEC = {
    "small": ["mp4v", '.mp4'],
    "normal": ["DIVX", '.avi'],
    "lossless": ["HFYU", '.avi'],
}

# Error level
FATAL_ERROR = 4
ERROR = 3
WARNING = 2
INFOMATION = 1
IGNORE = 0
# # Dealing level
# ERR_LEVEL_OFF = 0   # Ignore All.
# ERR_LEVEL_FATAL = 1 # Only deal with FATAL_ERROR.
# ERR_LEVEL_ERROR = 2 # Only deal with ERROR.
# ERR_LEVEL_WARN = 4  # Onle deal with WARNING.
# ERR_LEVEL_INFO = 8  # Only deal with INFOMATION.
# ERR_LEVEL_ALL = 16  # Deal with all things.


@unique
class colors(Enum):
    Red = (0, 0, 255)
    Green = (0, 255, 0)
    Blue = (255, 0, 0)
    White = (255, 255, 255)
    Black = (0, 0, 0)


def report(err, msg, err_level_adj=None):
    if err_level_adj is not None:
        err += err_level_adj
    else:
        err += os.environ.get('ERROR_LEVEL_ADJ', default=0)
    if err is FATAL_ERROR:
        raise SystemError("[!!!]"+str(msg))
    elif err is ERROR:
        raise RuntimeError(msg)
    elif err is WARNING:
        from warnings import warn
        warn('[!]'+str(msg))
    elif err is INFOMATION:
        print('[i]'+str(msg))
    elif err is IGNORE:
        pass


# from datetime import datetime


class chronograph:
    status = Enum('status', ('init', 'start', 'pause', 'finish', 'stop'))

    # class status(Enum):
    #     init = 0
    #     start = 1
    #     pause = 2
    #     finish = 3
    #     stop = 4

    def __init__(self, totaltime=0):
        self.__status__ = status.init
        self._init = now()

    def start(self):
        self.__status__ = status.start
        self._start = now()

    def restart(self):
        self.__status__ = status.start
        self._start = now()

    def stop(self):
        self.__status__ = status.stop
        self._stop = now()

    def pause(self):
        self.__status__ = status.pause
        pass

    @property
    def onFinish(self):
        pass

    @onFinish.setter
    def onFinish(self, value):
        pass

    @property
    def totaltime(self):
        return self._totaltime

    @totaltime.setter
    def totaltime(self, value):
        self._totaltime = value

    @property
    def elapsed(self):
        elapsed = now()-self._start
        if elapsed >= self._totaltime:
            self._finish = True
        return elapsed
