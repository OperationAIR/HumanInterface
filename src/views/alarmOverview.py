
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

class AlarmOverview(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback

    def fill_frame(self):
        print("Filling frame!")

        close_btn = FlatButton(self, self.callback, SettingType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)