
import tkinter as tk
from tkinter import StringVar, Button, Frame, Label
import matplotlib

matplotlib.use("TkAgg")
from tkinter import ttk, BOTH, N, S, E, W, LEFT
import tkinter.font as tkFont

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.constants import SettingType


import enum

class ButtonAction (enum.Enum):
    NONE = 0
    MINUS = 1
    PLUS = 2

class ChangeSingleSettingView(Frame):

    def __init__(self, type, current, min, max, step, description, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.type = type

        self.current = current
        self.min = min
        self.max = max
        self.step = step
        self.description = description
        self.callback = callback

        self.fill_frame()

    def confirmSetting(self, type):
        self.callback(type, self.current)

    def valueChange(self, action):
        if action == ButtonAction.MINUS and self.current - self.step >= self.min:
            self.current = self.current - self.step
        elif action == ButtonAction.PLUS and self.current + self.step <= self.max:
            self.current = self.current + self.step

        self.value_btn.setText(self.current)

    def fill_frame(self):

        pad = 1

        close_btn = FlatButton(self, self.confirmSetting, SettingType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=3, sticky=N+S+E+W, padx=10, pady=10)

        desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=20)
        desc_btn.setText(self.description)
        desc_btn.grid(row=1, column=0, sticky=N + S + E + W)

        minus_btn = FlatButton(self, self.valueChange, ButtonAction.MINUS,
                                  self.config.values['colors']['lightBlue'], fontSize=30)
        minus_btn.setText("-")
        minus_btn.grid(row=1, column=1, sticky=N + S + E + W, padx=pad, pady=80)

        plus_btn = FlatButton(self, self.valueChange, ButtonAction.PLUS,
                                 self.config.values['colors']['lightBlue'], fontSize=30)
        plus_btn.setText("+")
        plus_btn.grid(row=1, column=2, sticky=N + S + E + W, padx=pad, pady=80)

        self.value_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        self.value_btn.setText(self.current)
        self.value_btn.grid(row=1, column=3, sticky=N + S + E + W)


        confirm_btn = FlatButton(self, self.confirmSetting, self.type, self.config.values['colors']['green'], fontSize=40)
        confirm_btn.setText("Confirm", "white")
        confirm_btn.grid(row=2, column=0, columnspan=4, sticky=N + S + E + W, padx=20, pady=(20, 20))

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=2)