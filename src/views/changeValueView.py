
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

class ChangeValueViewActions(enum.Enum):
    BACK = 1

class ChangeValueView(Frame):

    def __init__(self, width, height, settings, callback, parent=None):
        Frame.__init__(self, parent, width=width, height=height, bg="black")
        self.settings = settings
        self.callback = callback

        self.fill_frame()

    def fill_frame(self):
        air_btn = Button(self, text="BACK", background='#263655', highlightbackground='#161E2E',
                         foreground='white', command=lambda: self.callback(ChangeValueViewActions.BACK))
        air_btn.grid(row=0, column=0, sticky=N + S + E + W)