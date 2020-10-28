#! /usr/bin/env python
# by qxsoftware@163.com, 2020-10-27
# refer to https://github.com/QixuanAI/cvutils

from datetime import datetime, timedelta

now = datetime.now


class Job:

    def __init__(self, callback, *args):
        self.callback = callback
        self._args = args
        self._timeval = 0   # a temporary value waiting for time unit
        self._repeat = 0    # repeat times
        self._waittime = timedelta(0)   # wait time up to first callback
        self._calltime = now()  # time to callback
        self._interval = timedelta(0)   # time interval between every repeat
        self._finished = False

    def after(self, timeval):
        self._timeval = timeval
        self._settingTime = self.after
        return self

    def repeat(self, times):
        self._repeat=times
        return self

    def withInterval(self, interval):
        self._timeval = interval
        self._settingTime = self.withInterval
        return self

    def withParam(self, *args):
        self._args = args

    def update(self):
        if now() >= self._calltime:
            if self._repeat > 0:
                self._repeat -= 1
                self._calltime = now()+self._interval
            self.callback(*self._args)
            if self._repeat == 0:
                self._finished = True

    @property
    def isFinished(self):
        return self._finished

    def __setTime(self, delta):
        if self._settingTime == self.after:
            self._waittime = delta
            self._calltime = now() + self._waittime
        elif self._settingTime == self.withInterval:
            self._interval = delta
        else:
            raise RuntimeError(
                "Please call 'after()' or 'withInterval()' before select the unit of time.")
        self._settingTime = None
        return self

    @property
    def days(self):
        return self.__setTime(timedelta(days=self._timeval))

    @property
    def hours(self):
        return self.__setTime(timedelta(hours=self._timeval))

    @property
    def minutes(self):
        return self.__setTime(timedelta(minutes=self._timeval))

    @property
    def seconds(self):
        return self.__setTime(timedelta(seconds=self._timeval))

    @property
    def milliseconds(self):
        return self.__setTime(timedelta(milliseconds=self._timeval))


class schedule:

    def __init__(self):
        self._jobs = []
        self._async_jobs = []

    def I_Will_Do(self, callback, *args):
        job = Job(callback, *args)
        self._jobs.append(job)
        return job

    def Call_Me_to_Do(self, callback, *args):
        # todo
        raise NotImplementedError
        job = Job(callback, *args)
        self._async_jobs.append(job)
        return job

    def update(self):
        for job in self._jobs:
            job.update()
            if job.isFinished:
                self._jobs.remove(job)

    @property
    def isFinishedAll(self):
        return len(self._jobs) == 0

    @property
    def remainJobNum(self):
        return len(self._jobs)


if __name__ == "__main__":

    count = 0
    def printjob(msg1, msg2):
        global count
        count += 1
        print(msg1, msg2, now())
    sched = schedule()
    sched.I_Will_Do(printjob).after(3).seconds.repeat(5).withInterval(1).seconds.withParam(count,"Now is")
    sched.I_Will_Do(printjob,2,'time').withInterval(1).seconds.repeat(8)
    while not sched.isFinishedAll:
        sched.update()
