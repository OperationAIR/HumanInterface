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

    def __init__(self, width, height, settings, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, width=width, height=height, bg=self.config.values['colors']['darkBlue'])
        self.settings = settings
        self.callback = callback

        self.fill_frame()

    def update(self, settings):
        self.settings = settings

    def getFrame(self):
        return self.frame

    def fill_frame(self):
        air_btn = FlatButton(self, self.callback, MainViewActions.QUIT,
                             self.config.values['colors']['lightBlue'])
        air_btn.setText("OperationAIR")
        air_btn.grid(row=0, column=0, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        alarm_btn = FlatButton(self, self.callback, MainViewActions.ALARM, self.config.values['colors']['lightBlue'])
        alarm_btn.setText("Alarm")
        alarm_btn.grid(row=0, column=1, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        alarm_name_btn = FlatButton(self, self.callback, MainViewActions.VIEW_ALARMS, self.config.values['colors']['lightBlue'])
        alarm_name_btn.setText("Alarm Overview")
        alarm_name_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=(0,2), pady=2)

        patient_btn = FlatButton(self, self.callback, MainViewActions.PATIENT, self.config.values['colors']['lightBlue'])
        patient_btn.setText("Patient")
        patient_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=(0,2), pady=2)

        switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'])
        switch_btn.setText("Start")
        switch_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=(0,2), pady=2)

        peep_btn = FlatButton(self, self.callback, MainViewActions.PEEP, self.config.values['colors']['lightBlue'], fontSize=20)
        peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        peep_btn.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        freq_btn = FlatButton(self, self.callback, MainViewActions.FREQ, self.config.values['colors']['lightBlue'], fontSize=20)
        freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        freq_btn.grid(row=2, column=0,columnspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        tv_btn = FlatButton(self, self.callback, MainViewActions.TIDAL, self.config.values['colors']['lightBlue'], fontSize=20)
        tv_btn.setText("Tidal Volume" + '\n' + str() + " [mL]")
        tv_btn.grid(row=3, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        pres_btn = FlatButton(self, self.callback, MainViewActions.PRESSURE, self.config.values['colors']['lightBlue'], fontSize=20)
        pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        pres_btn.grid(row=4, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        oxy_btn = FlatButton(self, self.callback, MainViewActions.OXYGEN, self.config.values['colors']['lightBlue'], fontSize=20)
        oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")
        oxy_btn.grid(row=5, column=0, columnspan=2,sticky=N + S + E + W,padx=(0,2), pady=(2,0))

        for i in range(0, 6):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)