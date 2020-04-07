
import tkinter as tk
from tkinter import StringVar, Button, Frame, Label
import matplotlib

matplotlib.use("TkAgg")
from tkinter import ttk, BOTH, N, S, E, W, LEFT
import tkinter.font as tkFont

from utils.config import ConfigValues
from utils.flatButton import FlatButton


import enum

class AlarmType(enum.Enum):
    NONE = 0
    PEEP = 1
    PRESSURE = 2
    TIDAL = 3
    OXYGEN = 4

class ChangeAlarmViewActions(enum.Enum):
    CONFIRM = 2
    MINMINUS = 3
    MINPLUS = 4
    MAXMINUS = 5
    MAXPLUS = 6

class ChangeAlarmSettingsView(Frame):

    def __init__(self, type, min_current, min_min, min_max, max_current, max_min, max_max, step, description, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.type = type

        self.min_current = min_current
        self.min_min = min_min
        self.min_max = min_max

        self.max_current = max_current
        self.max_min = max_min
        self.max_max = max_max
        self.step = step
        self.description = description
        self.callback = callback

        self.fill_frame()

    def confirmSetting(self, type):
        self.callback(type, self.min_current, self.max_current)

    def valueChange(self, action):
        if action == ChangeAlarmViewActions.MINMINUS and self.min_current - self.step >= self.min_min:
            self.min_current = self.min_current - self.step
        elif action == ChangeAlarmViewActions.MINPLUS and self.min_current + self.step <= self.min_max and self.max_current - self.min_current > self.step:
            self.min_current = self.min_current + self.step
        elif action == ChangeAlarmViewActions.MAXMINUS and self.max_current - self.step >= self.max_min and self.max_current - self.min_current > self.step:
            self.max_current = self.max_current - self.step
        elif action == ChangeAlarmViewActions.MAXPLUS and self.max_current + self.step <= self.max_max:
            self.max_current = self.max_current + self.step

        self.min_value_btn.setText(self.min_current)
        self.max_value_btn.setText(self.max_current)

    def fill_frame(self):

        pad = 1

        desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        desc_btn.setText(self.description)
        desc_btn.grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)

        close_btn = FlatButton(self, self.confirmSetting, AlarmType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=3, sticky=N+S+E+W, padx=10, pady=10)

        min_desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=20)
        min_desc_btn.setText("Minimum Value")
        min_desc_btn.grid(row=1, column=0, sticky=N + S + E + W)

        minminus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MINMINUS,
                                  self.config.values['colors']['lightBlue'], fontSize=30)
        minminus_btn.setText("-")
        minminus_btn.grid(row=1, column=1, sticky=N + S + E + W, padx=pad, pady=pad)

        minplus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MINPLUS,
                                 self.config.values['colors']['lightBlue'], fontSize=30)
        minplus_btn.setText("+")
        minplus_btn.grid(row=1, column=2, sticky=N + S + E + W, padx=pad, pady=pad)

        self.min_value_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        self.min_value_btn.setText(self.min_current)
        self.min_value_btn.grid(row=1, column=3, sticky=N + S + E + W)

        max_desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=20)
        max_desc_btn.setText("Maximum Value")
        max_desc_btn.grid(row=2, column=0, sticky=N + S + E + W)

        maxminus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MAXMINUS,
                                  self.config.values['colors']['lightBlue'], fontSize=30)
        maxminus_btn.setText("-")
        maxminus_btn.grid(row=2, column=1, sticky=N + S + E + W,padx=pad, pady=pad)

        maxplus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MAXPLUS,
                                 self.config.values['colors']['lightBlue'], fontSize=30)
        maxplus_btn.setText("+")
        maxplus_btn.grid(row=2, column=2, sticky=N + S + E + W,padx=pad, pady=pad)

        self.max_value_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        self.max_value_btn.setText(self.max_current)
        self.max_value_btn.grid(row=2, column=3, sticky=N + S + E + W)

        confirm_btn = FlatButton(self, self.confirmSetting, self.type, self.config.values['colors']['green'], fontSize=40)
        confirm_btn.setText("Confirm", "white")
        confirm_btn.grid(row=3, column=0, columnspan=4, sticky=N + S + E + W, padx=20, pady=(60, 20))

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)
        for i in range(1, 4):
            self.rowconfigure(i, weight=2)