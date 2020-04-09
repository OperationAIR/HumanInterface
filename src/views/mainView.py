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
from tkinter import ttk, BOTH, X, Y, N, S, E, W

from models.mcuSensorModel import Sensors

from controllers.alarmController import AlarmController, AlarmType

from utils.config import ConfigValues
from utils.flatButton import FlatButton

from views.graphView import GraphView


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

    def getBtnColor(self, low_alarm, high_alarm):
        if self.alarms.hasActiveAlarm(low_alarm) or self.alarms.hasActiveAlarm(high_alarm):
            return self.config.values['colors']['alarmColor']
        return self.config.values['colors']['lightBlue']


    def update(self, settings, sensordata):
        self.settings = settings
        self.sensordata = sensordata

        if not self.oxy_btn:
            return

        start_stop_text = "START"
        if self.settings.start:
            start_stop_text = "STOP"

        if self.alarms.present():
            self.alarm_overview_btn.setBackground(self.config.values['colors']['alarmColor'])
        else:
            self.alarm_overview_btn.setBackground()

        self.switch_btn.setText(start_stop_text)
        self.peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.peep_btn.setBackground(self.getBtnColor(AlarmType.PEEP_TOO_LOW, AlarmType.PEEP_TOO_HIGH))
        self.freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.tv_btn.setText("Tidal Volume\n"+str(self.sensordata.minute_volume)+" [L/min]\n"+str(self.sensordata.tidal_volume_exhale)+" [mL]")
        self.tv_btn.setBackground(self.getBtnColor(AlarmType.TIDAL_TOO_LOW, AlarmType.TIDAL_TOO_HIGH))
        self.pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.pres_btn.setBackground(self.getBtnColor(AlarmType.PRESSURE_TOO_LOW, AlarmType.PRESSURE_TOO_HIGH))
        self.oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]\n" + str(self.sensordata.oxygen) + "[%]")
        self.oxy_btn.setBackground(self.getBtnColor(AlarmType.OXYGEN_TOO_LOW, AlarmType.OXYGEN_TOO_HIGH))

        self.flowgraph.update(-1 * self.sensordata.flow)
        self.pressuregraph.update(self.sensordata.pressure)
        self.tidalgraph.update(self.sensordata.tidal_volume_exhale)

    def getFrame(self):
        return self.frame


    def drawGraphs(self):


        # Parameters
        pressure_x_len = 400         # Number of points to display
        pressure_y_range = [0, 80]  # Range of possible Y values to display

        self.pressuregraph = GraphView("Pressure", "[cm H2O]", self.sensordata.pressure, pressure_y_range, pressure_x_len, self.config.values['colors']['pressurePlot'], self)
        self.pressuregraph.getPlot().grid(row=1, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)

        # Parameters
        flow_x_len = 400         # Number of points to display
        flow_y_range = [-30, 0]  # Range of possible Y values to display

        self.flowgraph = GraphView("Flow", "[L / min]", self.sensordata.flow, flow_y_range, flow_x_len, self.config.values['colors']['flowPlot'], self)
        self.flowgraph.getPlot().grid(row=6, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)

        # Parameters
        tidal_x_len = 400  # Number of points to display
        tidal_y_range = [0, 80]  # Range of possible Y values to display

        self.tidalgraph = GraphView("Tidal Volume", "[mL]", self.sensordata.tidal_volume_exhale, tidal_y_range,
                               tidal_x_len, self.config.values['colors']['green'], self)
        self.tidalgraph.getPlot().grid(row=11, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)


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
        self.alarm_overview_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.patient_btn = FlatButton(self, self.callback, MainViewActions.PATIENT, self.config.values['colors']['lightBlue'])
        self.patient_btn.setText("Patient")
        self.patient_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=(0,2), pady=(2, 0))

        self.switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'])
        self.switch_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=(0,2), pady=(2, 0))

        self.peep_btn = FlatButton(self, self.callback, MainViewActions.PEEP, self.config.values['colors']['lightBlue'])
        self.peep_btn.grid(row=1, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.freq_btn = FlatButton(self, self.callback, MainViewActions.FREQ, self.config.values['colors']['lightBlue'])
        self.freq_btn.grid(row=4, column=0,columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.tv_btn = FlatButton(self, self.callback, MainViewActions.TIDAL, self.config.values['colors']['lightBlue'])
        self.tv_btn.grid(row=7, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.pres_btn = FlatButton(self, self.callback, MainViewActions.PRESSURE, self.config.values['colors']['lightBlue'])
        self.pres_btn.grid(row=10, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.oxy_btn = FlatButton(self, self.callback, MainViewActions.OXYGEN, self.config.values['colors']['lightBlue'])
        self.oxy_btn.grid(row=13, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))


        # plotPressureFrame = Frame(self, bg='green')
        # plotPressureFrame.grid(row=6, column=2, columnspan=3, rowspan=5, sticky=N+S+E+W)
    
        self.rowconfigure(0, weight=5)
        for i in range(1, 17):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)

        self.drawGraphs()

