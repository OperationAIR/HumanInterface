import os
import time
from enum import IntEnum
from pathlib import Path

import pygame
from utils.airTime import AirTime
from utils.anamolyDetection import Anomaly, check_for_anomalies
from utils.internationalization import Internationalization

ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

pygame.mixer.init()

mediumAlarm = pygame.mixer.Sound(ROOT_DIR + "/resources/sounds/medium_alarm.wav")
#highAlarm = pygame.mixer.Sound("alarm_high_priority.wav")

Internationalization()

AlarmString = [
    _("Nothing."),
    _("Clear all alarms"),
    _("PEEP value too high"),
    _("PEEP value too low"),
    _("TIDAL value too high"),
    _("TIDAL value too low"),
    _("PRESSURE value too high"),
    _("PRESSURE value too low"),
    _("OXYGEN value too high"),
    _("OXYGEN value too low")
]

class AlarmType(IntEnum):
    NONE = 0
    CLEAR = 1
    PEEP_TOO_HIGH = 2
    PEEP_TOO_LOW = 3
    TIDAL_TOO_HIGH = 4
    TIDAL_TOO_LOW = 5
    PRESSURE_TOO_HIGH = 6
    PRESSURE_TOO_LOW = 7
    OXYGEN_TOO_LOW = 8
    OXYGEN_TOO_HIGH = 9

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
        self.airTime = AirTime()
        self.timestamp = self.airTime.time
        self.count = 1
        self.active = True

    def newOccurence(self):
        self.count += 1
        self.active = True
        self.timestamp = self.airTime.time

    def turnOff(self):
        self.active = False

    def turnOn(self):
        self.active = True

    def __str__(self):
        return AlarmString[(self.type)] + " (" + _("Latest at") + " " + self.timestamp + ")"

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
            for alarm in self.alarms:
                if alarm.active:
                    return True
            return False

        def hasActiveAlarm(self, type):
            for alarm in self.alarms:
                if alarm.type == type and alarm.active:
                    return True
            return False

        def printAlarms(self):
            for alarm in self.alarms:
                print(str(alarm))

        def removeInactive(self):
            self.alarms[:] = [alarm for alarm in self.alarms if alarm.active]
            print(len(self.alarms))

        def checkAlarm(self, actual, min, max, low_type, high_type):
            if min > actual:
                self.addAlarm(low_type)
                return True
            elif max < actual:
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
