import os
from enum import IntEnum
from pathlib import Path

import pygame
from models.mcuSensorModel import UPSStatus

from utils.airTime import AirTime
from utils.anamolyDetection import Anomaly, check_for_anomalies
from utils.internationalization import Internationalization
from utils.config import ConfigValues

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
    _("OXYGEN value too low"),
    _("Running on BATTERY"),
    _("LOW BATTERY"),
    _("Controller disconnected")
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
    OXYGEN_TOO_HIGH = 8
    OXYGEN_TOO_LOW = 9
    RUN_ON_BATTERY = 10
    LOW_BATTERY = 11
    MCU_DISCONNECTED = 12

def registerAlarm():
    if pygame.mixer.get_busy() == 1:
        pass
    else:
        mediumAlarm.play()

def stopAlarm():
    pygame.mixer.pause()


class Alarm:
    def __init__(self, atype):
        self.type = atype
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
            self.started_since = -1
            config = ConfigValues()
            self.timeout = config.values['alarmSettings']['alarm_start_delay']
            self.airTime = AirTime()

        def addAlarm(self, atype):
            found = False
            for alarm in self.alarms:
                if alarm.type == atype:
                    alarm.newOccurence()
                    found = True

            if not found:
                self.alarms.append(Alarm(atype))

            registerAlarm()

        def present(self):
            for alarm in self.alarms:
                if alarm.active:
                    return True
            return False

        def hasActiveAlarm(self, atype):
            for alarm in self.alarms:
                if alarm.type == atype and alarm.active:
                    return True
            return False

        def printAlarms(self):
            for alarm in self.alarms:
                print(str(alarm))

        def removeInactive(self):
            self.alarms[:] = [alarm for alarm in self.alarms if alarm.active]

        def removeAlarm(self, atype):
            [self.alarms.remove(a) for a in self.alarms if atype == a.type]
            self.mute(atype)

        def checkAlarm(self, actual, min, max, low_type, high_type):
            if min > actual:
                self.addAlarm(low_type)
                return True
            elif max < actual:
                self.addAlarm(high_type)
                return True
            return False

        def mute(self, atype):
            activeAlarm = False
            for alarm in self.alarms:
                activeAlarm = alarm.active or activeAlarm
                if alarm.type == atype:
                    alarm.turnOff()

            if not activeAlarm:
                stopAlarm()

        def resetStartDelay(self):
            self.started_since = -1


        def checkStartDelay(self, settings):
            if settings.start and self.started_since == -1:
                self.started_since = self.airTime.time_in_seconds
                return False

            if self.started_since == -1:
                return False

            return self.airTime.time_in_seconds - self.started_since >= self.timeout


        def checkForNewAlarms(self, settings, sensordata):

            can_start = self.checkStartDelay(settings)

            if not can_start:
                return

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

            if sensordata.battery_percentage < settings.min_batt:
                self.addAlarm(AlarmType.LOW_BATTERY)
            
            if sensordata.ups_status == UPSStatus.BATTERY_POWERED:
                self.addAlarm(AlarmType.RUN_ON_BATTERY)
            elif sensordata.ups_status == UPSStatus.OK:
                self.removeAlarm(AlarmType.RUN_ON_BATTERY)


        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not AlarmController.instance:
            AlarmController.instance = AlarmController.__AlarmController()

    def __getattr__(self, name):
        return getattr(self.instance, name)
