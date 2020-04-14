
import tkinter as tk
from tkinter import StringVar, Button, Frame, Label
import matplotlib

matplotlib.use("TkAgg")
from tkinter import ttk, BOTH, N, S, E, W, LEFT
import tkinter.font as tkFont

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.constants import SettingType

from views.graphView import GraphView

from controllers.alarmController import AlarmController, AlarmType


import enum

class HistoryViewActions(enum.Enum):
    CLOSE = 0
    ONE_HOUR = 1
    SIX_HOUR = 2
    TWELVE_HOUR = 3
    TWENTY_FOUR_HOUR = 4
    SEVENTY_TWO_HOUR = 5
    DELETE = 6
    FLOW = 7
    PRESSURE = 8
    TIDAL = 9
    OXYGEN = 10

class HistoryView(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback

    def fill_frame(self):

        patient_text = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=20)
        patient_text.setText("Patient History")
        patient_text.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W, padx=10, pady=20)

        one_hour_btn = FlatButton(self, self.callback, HistoryViewActions.ONE_HOUR,
                                  self.config.values['colors']['lightBlue'], fontSize=20)
        one_hour_btn.setText("1u")
        one_hour_btn.grid(row=0, column=2, sticky=N+S+E+W, padx=10, pady=20)

        six_hour_btn = FlatButton(self, self.callback, HistoryViewActions.SIX_HOUR,
                                  self.config.values['colors']['lightBlue'], fontSize=20)
        six_hour_btn.setText("6u")
        six_hour_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=20)

        twelve_hour_btn = FlatButton(self, self.callback, HistoryViewActions.TWELVE_HOUR,
                       self.config.values['colors']['lightBlue'], fontSize=20)
        twelve_hour_btn.setText("12u")
        twelve_hour_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=10, pady=20)

        twenty_four_hour_btn = FlatButton(self, self.callback, HistoryViewActions.TWENTY_FOUR_HOUR,
                                  self.config.values['colors']['lightBlue'], fontSize=20)
        twenty_four_hour_btn.setText("24u")
        twenty_four_hour_btn.grid(row=0, column=5, sticky=N + S + E + W, padx=10, pady=20)

        seventy_two_hour_btn = FlatButton(self, self.callback, HistoryViewActions.SEVENTY_TWO_HOUR,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        seventy_two_hour_btn.setText("1u")
        seventy_two_hour_btn.grid(row=0, column=6, sticky=N + S + E + W, padx=10, pady=20)

        delete_btn = FlatButton(self, self.callback, HistoryViewActions.DELETE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        delete_btn.setText("Delete")
        delete_btn.grid(row=0, column=7, sticky=N + S + E + W, padx=10, pady=20)

        close_btn = FlatButton(self, self.callback, HistoryViewActions.CLOSE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText("Close")
        close_btn.grid(row=0, column=8, sticky=N + S + E + W, padx=10, pady=20)

        flow_btn = FlatButton(self, self.callback, HistoryViewActions.FLOW,
                                          self.config.values['colors']['lightBlue'], fontSize=20)
        flow_btn.setText("Flow")
        flow_btn.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W, padx=10, pady=20)

        pressure_btn = FlatButton(self, self.callback, HistoryViewActions.PRESSURE,
                              self.config.values['colors']['lightBlue'], fontSize=20)
        pressure_btn.setText("Pressure")
        pressure_btn.grid(row=1, column=2, columnspan=2, sticky=N + S + E + W, padx=10, pady=20)

        tidal_btn = FlatButton(self, self.callback, HistoryViewActions.TIDAL,
                                  self.config.values['colors']['lightBlue'], fontSize=20)
        tidal_btn.setText("Tidal Volume")
        tidal_btn.grid(row=1, column=5, columnspan=2, sticky=N + S + E + W, padx=10, pady=20)

        oxy_btn = FlatButton(self, self.callback, HistoryViewActions.OXYGEN,
                                  self.config.values['colors']['lightBlue'], fontSize=20)
        oxy_btn.setText("Oxygen")
        oxy_btn.grid(row=1, column=7, columnspan=2, sticky=N + S + E + W, padx=10, pady=20)

        # Parameters
        pressure_x_len = 400         # Number of points to display
        pressure_y_range = [0, 80]  # Range of possible Y values to display

        self.historygraph = GraphView("Pressure", "[cm H2O]", 0, pressure_y_range, pressure_x_len, self.config.values['colors']['pressurePlot'], self)
        self.historygraph.getPlot().grid(row=2, column=0, rowspan=5, columnspan=8, sticky=N + S + E + W)



        for i in range(0, 9):
            self.columnconfigure(i, weight=1)

        for i in range(0, 7):
            self.rowconfigure(i, weight=1)
