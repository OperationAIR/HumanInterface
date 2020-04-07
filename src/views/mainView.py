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
        Frame.__init__(self, parent, width=width, height=height, bg="black")
        self.settings = settings
        self.callback = callback

        self.fill_frame()

    def update(self, settings):
        self.settings = settings

    def getFrame(self):
        return self.frame

    def fill_frame(self):
        air_btn_text = StringVar()
        air_btn_text.set("OperationAir")
        air_btn = Button(self, textvariable=air_btn_text, background='#263655', highlightbackground='#161E2E',
                         foreground='white', command=lambda: self.callback(MainViewActions.QUIT))
        air_btn.grid(row=0, column=0, sticky=N + S + E + W)
        #
        self.alarm_btn_text = StringVar()
        self.alarm_btn_text.set("Alarm")
        self.alarm_btn = Button(self, textvariable=self.alarm_btn_text, background='#263655',
                                highlightbackground='#161E2E', foreground='white',
                                command=lambda: self.callback(MainViewActions.ALARM))
        self.alarm_btn.grid(row=0, column=1, sticky=N + S + E + W)

        self.alarm_name_btn_text = StringVar()
        self.alarm_name_btn_text.set("Alarm overview")
        self.alarm_name_btn = Button(self, textvariable=self.alarm_name_btn_text, background='#263655',
                                     highlightbackground='#161E2E', foreground='white',
                                     command=lambda: self.callback(MainViewActions.VIEW_ALARMS))
        self.alarm_name_btn.grid(row=0, column=2, sticky=N + S + E + W)

        self.patient_btn_text = StringVar()
        self.patient_btn_text.set("Patient")
        self.patient_btn = Button(self, textvariable=self.patient_btn_text, background='#263655',
                                  highlightbackground='#161E2E', foreground='white',
                                  comman=lambda: self.callback(MainViewActions.PATIENT))
        self.patient_btn.grid(row=0, column=3, sticky=N + S + E + W)

        self.switch_btn_text = StringVar()
        self.switch_btn_text.set("Start")
        self.switch_btn = Button(self, textvariable=self.switch_btn_text, background='#263655',
                                 highlightbackground='#161E2E', foreground='white', command=lambda: self.callback(MainViewActions.STARTSTOP))
        self.switch_btn.grid(row=0, column=4, sticky=N + S + E + W)

        self.peep_btn_text = StringVar()
        self.peep_btn_text.set("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.peep_btn = Button(self, textvariable=self.peep_btn_text, background='#263655',
                               highlightbackground='#161E2E', foreground='white',
                               command=lambda: self.callback(MainViewActions.PEEP))
        self.peep_btn.grid(row=1, column=0, sticky=N + S + E + W)

        self.freq_btn_text = StringVar()
        self.freq_btn_text.set("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.freq_btn = Button(self, textvariable=self.freq_btn_text, background='#263655',
                               highlightbackground='#161E2E', foreground='white',
                               command=lambda: self.callback(MainViewActions.FREQ))
        self.freq_btn.grid(row=2, column=0, sticky=N + S + E + W)

        self.tv_btn_text = StringVar()
        self.tv_btn_text.set("Tidal Volume" + '\n' + str() + " [mL]")
        self.tv_btn = Button(self, textvariable=self.tv_btn_text, background='#263655',
                             highlightbackground='#161E2E', foreground='white')
        self.tv_btn.grid(row=3, column=0, sticky=N + S + E + W)

        self.pres_btn_text = StringVar()
        self.pres_btn_text.set("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.pres_btn = Button(self, textvariable=self.pres_btn_text, background='#263655',
                               highlightbackground='#161E2E', foreground='white',
                               command=lambda: self.callback(MainViewActions.PRESSURE))
        self.pres_btn.grid(row=4, column=0, sticky=N + S + E + W)

        self.oxy_btn_text = StringVar()
        self.oxy_btn_text.set("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")
        self.oxy_btn = Button(self, textvariable=self.oxy_btn_text, background='#263655',
                              highlightbackground='#161E2E', foreground='white',
                              command=lambda: self.callback(MainViewActions.OXYGEN))
        self.oxy_btn.grid(row=5, column=0, sticky=N + S + E + W)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)