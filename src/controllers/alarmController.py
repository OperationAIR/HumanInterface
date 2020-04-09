import pygame
import os
from pathlib import Path

from models.mcuSensorModel import Sensors
from models.mcuSettingsModel import Settings

from utils.anamolyDetection import Anomaly, check_for_anomalies

import enum
import time
from datetime import datetime

ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

pygame.mixer.init()
print(ROOT_DIR + "/resources/sounds/vent.wav")

mediumAlarm = pygame.mixer.Sound(ROOT_DIR + "/resources/sounds/vent.wav")
#highAlarm = pygame.mixer.Sound("alarm_high_priority.wav")

AlarmString = [
    "Nothing.",
    "PEEP value too high",
    "PEEP value too low",
    "TIDAL value too high",
    "TIDAL value too low",
    "PRESSURE value too high",
    "PRESSURE value too low",
    "OXYGEN value too high",
    "OXYGEN value too low"
]

class AlarmType(enum.IntEnum):
    NONE = 0
    PEEP_TOO_HIGH = 1
    PEEP_TOO_LOW = 2
    TIDAL_TOO_HIGH = 3
    TIDAL_TOO_LOW = 4
    PRESSURE_TOO_HIGH = 5
    PRESSURE_TOO_LOW = 6
    OXYGEN_TOO_LOW = 7
    OXYGEN_TOO_HIGH = 8

def registerAlarm():
    if pygame.mixer.get_busy() == 1:
        pass
    else:
        mediumAlarm.play()

def stopAlarm():
    pygame.mixer.pause()


class Alarm:
    def __init__(self, type):
        self.type = type
        self.timestamp = time.time()
        self.count = 1
        self.active = True

    def newOccurence(self):
        self.count += 1
        self.active = True
        self.timestamp = time.time()

    def turnOff(self):
        self.active = False

    def turnOn(self):
        self.active = True

    def __str__(self):
        dt_object = datetime.fromtimestamp(self.timestamp)
        return AlarmString[(self.type)] + " (Latest at " + str(dt_object.hour) +":" + str(dt_object.minute) + ")"

class AlarmController:

    class __AlarmController:
        def __init__(self):
            self.alarms = []

        def addAlarm(self, type):
            found = False
            for alarm in self.alarms:
                if alarm.type == type:
                    alarm.newOccurence()
                    found = True

            if not found:
                self.alarms.append(Alarm(type))

            registerAlarm()

        def present(self):
            return len(self.alarms) >= 1

        def printAlarms(self):
            for alarm in self.alarms:
                print(str(alarm))

        def checkAlarm(self, actual, min, max, low_type, high_type):
            if actual < min:
                self.addAlarm(low_type)
                return True
            elif max > actual:
                self.addAlarm(high_type)
                return True
            return False

        def mute(self, type):
            activeAlarm = False
            for alarm in self.alarms:
                activeAlarm = alarm.active or activeAlarm
                if alarm.type == type:
                    alarm.turnOff()

            if not activeAlarm:
                stopAlarm()


        def checkForNewAlarms(self, settings, sensordata):
            anomaly = check_for_anomalies(sensordata, settings)

            if anomaly == Anomaly.PEEP_TOO_HIGH:
                self.addAlarm(AlarmType.PEEP_TOO_HIGH)
            elif anomaly == Anomaly.PEEP_TOO_LOW:
                self.addAlarm(AlarmType.PEEP_TOO_LOW)
            elif anomaly == Anomaly.PRESS_TOO_LOW:
                self.addAlarm(AlarmType.PRESSURE_TOO_LOW)
            elif anomaly == Anomaly.PRESS_TOO_HIGH:
                self.addAlarm(AlarmType.PRESSURE_TOO_HIGH)

            self.checkAlarm(sensordata.tidal_volume_exhale, settings.min_tv, settings.max_tv, AlarmType.TIDAL_TOO_LOW,
                            AlarmType.TIDAL_TOO_HIGH)
            self.checkAlarm(sensordata.oxygen, settings.min_fio2, settings.max_fio2,
                            AlarmType.OXYGEN_TOO_LOW,
                            AlarmType.OXYGEN_TOO_HIGH)

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not AlarmController.instance:
            AlarmController.instance = AlarmController.__AlarmController()

    def __getattr__(self, name):
        return getattr(self.instance, name)
