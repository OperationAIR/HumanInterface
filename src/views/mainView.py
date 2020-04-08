import tkinter as tk
from tkinter import StringVar, Button, Frame
import signal

from utils.config import ConfigValues
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from queue import Queue
from tkinter import ttk, BOTH, N, S, E, W

from models.mcuSensorModel import Sensors

from controllers.alarmController import AlarmController

from utils.config import ConfigValues
from utils.flatButton import FlatButton


import enum

class MainViewActions(enum.Enum):
    QUIT = 1
    ALARM = 2
    VIEW_ALARMS = 3
    PATIENT = 4
    STARTSTOP = 5
    PEEP = 6
    FREQ = 7
    TIDAL = 8
    PRESSURE = 9
    OXYGEN = 10

class MainView(Frame):

    def __init__(self, width, height, settings, sensordata, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, width=width, height=height, bg=self.config.values['colors']['darkBlue'])
        self.settings = settings
        self.sensordata = sensordata
        self.callback = callback

        self.alarms = AlarmController()

        self.fill_frame()

    def update(self, settings, sensordata):
        self.settings = settings
        self.sensordata = sensordata

        if not self.oxy_btn:
            return

        start_stop_text = "START"
        if self.settings.start:
            start_stop_text = "STOP"

        if self.alarms.present():
            self.alarm_overview_btn.setBackground("red")
        else:
            self.alarm_overview_btn.setBackground()

        self.switch_btn.setText(start_stop_text)
        self.tv_btn.setText("Tidal Volume" + '\n' + str(self.sensordata.tidal_volume) + " [mL]")
        self.peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.tv_btn.setText("Tidal Volume" + '\n' + str(self.sensordata.tidal_volume) + " [mL]")
        self.pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")

        self.checkAlarm(self.tv_btn, self.sensordata.tidal_volume, self.settings.min_tv, self.settings.max_tv)

    def checkAlarm(self, button, actual_value, min_value, max_value):
        if min_value < actual_value < max_value:
            button.setBackground(button.color)
        else:
            button.setBackground("red")

    def getFrame(self):
        return self.frame

    def fill_frame(self):
        self.air_btn = FlatButton(self, self.callback, MainViewActions.QUIT,
                         self.config.values['colors']['lightBlue'])
        self.air_btn.setText("OperationAIR")
        self.air_btn.grid(row=0, column=0, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_btn = FlatButton(self, self.callback, MainViewActions.ALARM, self.config.values['colors']['lightBlue'])
        self.alarm_btn.setText("Alarm")
        self.alarm_btn.grid(row=0, column=1, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_overview_btn = FlatButton(self, self.callback, MainViewActions.VIEW_ALARMS, self.config.values['colors']['lightBlue'])
        self.alarm_overview_btn.setText("Alarm Overview")
        self.alarm_overview_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.patient_btn = FlatButton(self, self.callback, MainViewActions.PATIENT, self.config.values['colors']['lightBlue'])
        self.patient_btn.setText("Patient")
        self.patient_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'])
        self.switch_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.peep_btn = FlatButton(self, self.callback, MainViewActions.PEEP, self.config.values['colors']['lightBlue'], fontSize=20)
        self.peep_btn.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.freq_btn = FlatButton(self, self.callback, MainViewActions.FREQ, self.config.values['colors']['lightBlue'], fontSize=20)
        self.freq_btn.grid(row=2, column=0,columnspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.tv_btn = FlatButton(self, self.callback, MainViewActions.TIDAL, self.config.values['colors']['mediumBlue'], fontSize=20)
        self.tv_btn.grid(row=3, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        self.pres_btn = FlatButton(self, self.callback, MainViewActions.PRESSURE, self.config.values['colors']['lightBlue'], fontSize=20)
        self.pres_btn.grid(row=4, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        self.oxy_btn = FlatButton(self, self.callback, MainViewActions.OXYGEN, self.config.values['colors']['lightBlue'], fontSize=20)
        self.oxy_btn.grid(row=5, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        for i in range(0, 6):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)