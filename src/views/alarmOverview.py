
import tkinter as tk
from tkinter import StringVar, Button, Frame, Label
import matplotlib

matplotlib.use("TkAgg")
from tkinter import ttk, BOTH, N, S, E, W, LEFT
import tkinter.font as tkFont

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.constants import SettingType

from controllers.alarmController import AlarmController, AlarmType


import enum

class AlarmOverview(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback
        self.alarms = AlarmController()

    def fill_frame(self):
        self.grid_forget()

        close_btn = FlatButton(self, self.callback, AlarmType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=10)

        for i in range(0, len(self.alarms.alarms)):
            color = self.config.values['colors']['lightBlue']
            if self.alarms.alarms[i].active:
                color = self.config.values['colors']['alarmColor']

            alarm_btn = FlatButton(self, self.callback, self.alarms.alarms[i].type,
                              color, fontSize=20)
            alarm_btn.setText(self.alarms.alarms[i])
            alarm_btn.grid(row=i + 1, column=0, columnspan=4, sticky=N + S + E + W, padx=10, pady=10)

        for i in range(0, len(self.alarms.alarms) + 1):
            self.rowconfigure(i, weight=1)
        for i in range(0, 4):
            self.columnconfigure(i, weight=1)