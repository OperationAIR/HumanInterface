
import tkinter as tk
from tkinter import StringVar, Button, Frame, Label
import matplotlib

matplotlib.use("TkAgg")
from tkinter import ttk, BOTH, N, S, E, W, LEFT
import tkinter.font as tkFont

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.constants import SettingType

from views.mainView import MainViewActions


import enum

class MenuViewActions(enum.Enum):
    NONE = 0
    SHUTDOWN = 1
    SELF_TEST = 2


class MenuView(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback

    def fill_frame(self):
        print("Filling frame!")
        close_btn = FlatButton(self, self.callback, MenuViewActions.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=10, pady=20)

        exit_btn = FlatButton(self, self.callback, MenuViewActions.SHUTDOWN,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        exit_btn.setText("Shutdown")
        exit_btn.grid(row=1, column=2, sticky=N + S + E + W, padx=(40,0), pady=40)


        test_btn = FlatButton(self, self.callback, MenuViewActions.SELF_TEST,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        test_btn.setText("Self Test")
        test_btn.grid(row=1, column=0, sticky=N + S + E + W,padx=(1,0), pady=40)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        for i in range(0, 3):
            self.columnconfigure(i, weight=1)
