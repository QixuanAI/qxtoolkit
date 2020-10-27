# ! /usr/bin/env python
# by qxsoftware@163.com, 2020-10-27
# refer to https://github.com/QixuanAI/cvutils

from timeit import default_timer as now


class chronograph:
    def __init__(self):
        self._start = now()

    def reset_zero(self):
        self._start = now()

    @property
    def elapsed_time(self):
        return now() - self._start


if __name__ == "__main__":
    chrono = chronograph()
    N = 100000
    for i in range(N - 1):
        print(i, " - ", chrono.elapsed_time, end='\r')
    print(N, " - ", chrono.elapsed_time)
