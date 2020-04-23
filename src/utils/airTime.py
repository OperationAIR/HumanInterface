from datetime import datetime, timedelta
import time


class AirTime:

    class __AirTime:

        def __init__(self):
            print("hi")

            self.offset = 0
        def setTime(self, time):
            system_time = datetime.now()
            air_time = datetime.now().replace(hour = int(time[0:2]), minute=int(time[3:5]))

            difference = air_time - system_time
            self.offset = difference.seconds

        @property
        def time(self):
            now = datetime.now() + timedelta(0, self.offset)
            dt = now.strftime("%H:%M")
            return dt

        @property
        def time_in_seconds(self):
            now = datetime.now() + timedelta(0, self.offset)
            return time.mktime(now.timetuple())

    instance = None

    def __init__(self):
        if not AirTime.instance:
            AirTime.instance = AirTime.__AirTime()

    def __getattr__(self, name):
        return getattr(self.instance, name)
