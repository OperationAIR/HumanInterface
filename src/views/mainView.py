from tkinter import Frame, N, S, E, W

from utils.config import ConfigValues
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from collections import deque

from controllers.alarmController import AlarmController, AlarmType

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.currentValueCanvas import CurrentValueCanvas

from views.graphView import GraphView

from models.mcuSensorModel import UPSStatus


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
    MENU = 11
    INSP_HOLD = 12
    EXP_HOLD = 13

class MainView(Frame):

    def __init__(self, width, height, settings, sensordata, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, width=width, height=height, bg=self.config.values['colors']['darkBlue'])
        self.settings = settings
        self.sensordata = sensordata
        self.callback = callback

        self.pressureQueue = deque(maxlen=self.config.values['developer']['pressureQueueLen'])

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

        start_stop_text = ""
        if self.settings.start:
            self.switch_btn.timeout = 5
            self.switch_btn.checkTimeout()
            start_stop_text = "STOP"
        else:
            self.switch_btn.timeout = 0
            start_stop_text = "START"

        if self.alarms.present():
            self.alarm_overview_btn.setBackground(self.config.values['colors']['alarmColor'])
        else:
            self.alarm_overview_btn.setBackground()

        self.pressureQueue.append(self.sensordata.pressure)

        self.switch_btn.setText(start_stop_text)
        self.peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.peep_btn.setBackground(self.getBtnColor(AlarmType.PEEP_TOO_LOW, AlarmType.PEEP_TOO_HIGH))
        self.freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.pres_btn.setBackground(self.getBtnColor(AlarmType.PRESSURE_TOO_LOW, AlarmType.PRESSURE_TOO_HIGH))
        self.oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")
        self.oxy_btn.setBackground(self.getBtnColor(AlarmType.OXYGEN_TOO_LOW, AlarmType.OXYGEN_TOO_HIGH))

        ppeak = max(self.pressureQueue)
        self.ppeak_label.setText("Ppeak", ppeak)
        pmean = sum(self.pressureQueue)/len(self.pressureQueue)
        self.pmean_label.setText("Pmean", pmean)

        self.freq_label.setText("Freq.", 10) # not implemented yet, freq sensordata
        self.oxy_label.setText("O2", self.sensordata.oxygen)
        self.tv_label1.setText("TVmin.vol.", self.sensordata.minute_volume)

        batt_status = self.sensordata.ups_status
        if batt_status == UPSStatus.OK:
            self.batt_label.setText("Pwr. %", self.sensordata.battery_percentage)
        elif batt_status == UPSStatus.BATTERY_POWERED:
            self.batt_label.setText("Batt. %", self.sensordata.battery_percentage)
        else:
            self.batt_label.setTitle("Pwr. Err.")

        self.flowgraph.update(-1 * self.sensordata.flow)
        self.pressuregraph.update(self.sensordata.pressure)

    def getFrame(self):
        return self.frame


    def drawGraphs(self):


        # Parameters
        pressure_x_len = 400         # Number of points to display
        pressure_y_range = [0, 40]  # Range of possible Y values to display

        self.pressuregraph = GraphView("Pressure", "[cm H2O]", self.sensordata.pressure, pressure_y_range, pressure_x_len, self.config.values['colors']['pressurePlot'], self)
        self.pressuregraph.getPlot().grid(row=1, column=2, rowspan=4, columnspan=2, sticky=N + S + E + W)

        # Parameters
        flow_x_len = 400         # Number of points to display
        flow_y_range = [-60, 0]  # Range of possible Y values to display

        self.flowgraph = GraphView("Flow", "[L / min]", self.sensordata.flow, flow_y_range, flow_x_len, self.config.values['colors']['flowPlot'], self)
        self.flowgraph.getPlot().grid(row=5, column=2, rowspan=4, columnspan=2, sticky=N + S + E + W)


    def fill_frame(self):
        # Buttons on the  top and left
        self.air_btn = FlatButton(self, self.callback, MainViewActions.MENU,
                             self.config.values['colors']['lightBlue'])
        self.air_btn.setText("Menu")
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

        self.switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'], timeout=5)
        self.switch_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=(0,2), pady=(2, 0))

        self.peep_btn = FlatButton(self, self.callback, MainViewActions.PEEP, self.config.values['colors']['lightBlue'])
        self.peep_btn.grid(row=1, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.freq_btn = FlatButton(self, self.callback, MainViewActions.FREQ, self.config.values['colors']['lightBlue'])
        self.freq_btn.grid(row=4, column=0,columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.pres_btn = FlatButton(self, self.callback, MainViewActions.PRESSURE, self.config.values['colors']['lightBlue'])
        self.pres_btn.grid(row=7, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.oxy_btn = FlatButton(self, self.callback, MainViewActions.OXYGEN, self.config.values['colors']['lightBlue'])
        self.oxy_btn.grid(row=10, column=0, columnspan=2, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))


        # Labels on the right side next to the graphs
        self.ppeak_label = CurrentValueCanvas(self, "Ppeak", 100, self.config.values['colors']['pressurePlot'])
        self.ppeak_label.grid(row=1, column=4, rowspan=2, sticky=N + S + E + W)

        self.pmean_label = CurrentValueCanvas(self, "Pmean", 50, self.config.values['colors']['pressurePlot'])
        self.pmean_label.grid(row=3, column=4, rowspan=2, sticky=N + S + E + W)

        self.freq_label = CurrentValueCanvas(self, "Freq.", 9, self.config.values['colors']['flowPlot'])
        self.freq_label.grid(row=5, column=4, rowspan=2, sticky=N + S + E + W)

        self.oxy_label = CurrentValueCanvas(self, "O2", self.sensordata.oxygen, 'white')
        self.oxy_label.grid(row=7, column=4, rowspan=2, sticky=N + S + E + W)

        self.tv_label1 = CurrentValueCanvas(self, "TVmin.vol",
                                           [self.sensordata.tidal_volume_inhale, self.sensordata.tidal_volume_exhale],
                                           self.config.values['colors']['green'])
        self.tv_label1.grid(row=9, column=4, rowspan=2, sticky=N + S + E + W)

        self.batt_label = CurrentValueCanvas(self, "Batt. %", self.sensordata.battery_percentage, 'white')
        self.batt_label.grid(row=11, column=4, rowspan=2, sticky=N + S + E + W)

        # Buttons under graphs
        self.inspHold_btn = FlatButton(self, self.callback, MainViewActions.INSP_HOLD, self.config.values['colors']['lightBlue'])
        self.inspHold_btn.setText("Inspiration\nHold")
        self.inspHold_btn.grid(row=10, column=2, columnspan=1, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.expHold_btn = FlatButton(self, self.callback, MainViewActions.EXP_HOLD, self.config.values['colors']['lightBlue'])
        self.expHold_btn.setText("Expiration\nHold")
        self.expHold_btn.grid(row=10, column=3, columnspan=1, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))


        self.rowconfigure(0, weight=5)
        for i in range(1, 10):
            self.rowconfigure(i, weight=1)
        for i in range(9, 13):
            self.rowconfigure(i, weight=3)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=2)

        self.drawGraphs()

