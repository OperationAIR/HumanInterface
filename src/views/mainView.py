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

from utils.config import ConfigValues
from utils.flatButton import FlatButton


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

        self.fill_frame()

    def update(self, settings, sensordata):
        self.settings = settings
        self.sensordata = sensordata

        self.tv_btn.setText("Tidal Volume" + '\n' + str(self.sensordata.tidal_volume) + " [mL]")
        self.peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.tv_btn.setText("Tidal Volume" + '\n' + str(self.sensordata.tidal_volume) + " [mL]")
        self.pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")

    def getFrame(self):
        return self.frame


    def GraphPlotFlow(self):

        # Parameters
        x_len = 400         # Number of points to display
        y_range = [-30, 0]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure(figsize=(1,1))
        self.fig.patch.set_facecolor('#263655')
        ax = self.fig.add_subplot(1, 1, 1, facecolor='#263655')
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(0, x_len))
        ys = [0 for x in range(x_len)]

        ax.set_ylim(y_range)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.get_yaxis().tick_left()
        ax.yaxis.label.set_size(13)
        ax.yaxis.label.set_color('white')
        plt.setp(ax.get_xticklabels(), visible=False)

        plt.yticks(fontsize=13, color='white')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")
        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color= '#43DBA7')

        # Add labels
        plt.title('Flow', fontsize= 13, color="white")
        #plt.xlabel('Samples')
        plt.ylabel('[L/min]')


        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            if not self.settings.start:
                return line,
            # Add y to list
            ys.append(-1*self.latest_sensor_data.flow)
            # Limit y list to set number of items
            ys = ys[-x_len:]
            # Update line with new Y values
            line.set_ydata(ys)

            return line,
        # Set up plot to call animate() function periodically

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)
        # canvas.get_tk_widget().grid(row=1, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)
        self.flow_animation_ref = animation.FuncAnimation(self.fig,
           animate,
           fargs=(ys,),
           interval=100,
           blit=True)

    def GraphPlotPressure(self):

        # Parameters
        x_len = 400         # Number of points to display
        y_range = [0, 80]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure(figsize=(1,1))
        self.fig.patch.set_facecolor('#263655')
        ax = self.fig.add_subplot(1, 1, 1, facecolor='#263655')
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(0, x_len))
        ys = [0 for x in range(x_len)]

        ax.set_ylim(y_range)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.get_yaxis().tick_left()
        ax.yaxis.label.set_size(13)
        ax.yaxis.label.set_color('white')
        plt.setp(ax.get_xticklabels(), visible=False)

        plt.yticks(fontsize=13, color='white')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")
        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color= '#EBE1D0')

        # Add labels
        plt.title('Pressure', fontsize= 13, color="white")
        #plt.xlabel('Samples')
        plt.ylabel('[cm H2O]')

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            if not self.settings.start:
                return line,
            # Add y to list
            ys.append(self.latest_sensor_data.pressure)

            # Limit y list to set number of items
            ys = ys[-x_len:]
            # Update line with new Y values
            line.set_ydata(ys)

            return line,
        # Set up plot to call animate() function periodically

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # canvas.place(fill=BOTH, extend=1)
        self.canvas.get_tk_widget().grid(row=6, column=2, rowspan=5, columnspan=3, sticky=N + S + E + W)
        self.pressure_animation_ref = animation.FuncAnimation(self.fig,
            animate,
            fargs=(ys,),
            interval=100,
            blit=True)


    def fill_frame(self):

        self.air_btn = FlatButton(self, self.callback, MainViewActions.QUIT,
                             self.config.values['colors']['lightBlue'])
        self.air_btn.setText("OperationAIR")
        self.air_btn.grid(row=0, column=0, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_btn = FlatButton(self, self.callback, MainViewActions.ALARM, self.config.values['colors']['lightBlue'])
        self.alarm_btn.setText("Alarm")
        self.alarm_btn.grid(row=0, column=1, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_name_btn = FlatButton(self, self.callback, MainViewActions.VIEW_ALARMS, self.config.values['colors']['lightBlue'])
        self.alarm_name_btn.setText("Alarm Overview")
        self.alarm_name_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.patient_btn = FlatButton(self, self.callback, MainViewActions.PATIENT, self.config.values['colors']['lightBlue'])
        self.patient_btn.setText("Patient")
        self.patient_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'])
        self.switch_btn.setText("Start")
        self.switch_btn.grid(row=0, column=4, sticky=N + S + E + W, padx=(0,2), pady=2)

        self.peep_btn = FlatButton(self, self.callback, MainViewActions.PEEP, self.config.values['colors']['lightBlue'], fontSize=20)
        self.peep_btn.setText("PEEP" + '\n' + str(self.settings.peep) + " [cm H2O]")
        self.peep_btn.grid(row=1, column=0, columnspan=2, rowspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.freq_btn = FlatButton(self, self.callback, MainViewActions.FREQ, self.config.values['colors']['lightBlue'], fontSize=20)
        self.freq_btn.setText("Frequency" + '\n' + str(self.settings.freq) + " [1/min]")
        self.freq_btn.grid(row=3, column=0,columnspan=2, rowspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.tv_btn = FlatButton(self, self.callback, MainViewActions.TIDAL, self.config.values['colors']['lightBlue'], fontSize=20)
        self.tv_btn.setText("Tidal Volume" + '\n' + str() + " [mL]")
        self.tv_btn.grid(row=5, column=0, columnspan=2, rowspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.pres_btn = FlatButton(self, self.callback, MainViewActions.PRESSURE, self.config.values['colors']['lightBlue'], fontSize=20)
        self.pres_btn.setText("Pressure" + '\n' + str(self.settings.pressure) + " [cm H2O]")
        self.pres_btn.grid(row=7, column=0, columnspan=2, rowspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.oxy_btn = FlatButton(self, self.callback, MainViewActions.OXYGEN, self.config.values['colors']['lightBlue'], fontSize=20)
        self.oxy_btn.setText("Oxygen (02)" + '\n' + str(self.settings.oxygen) + " [%]")
        self.oxy_btn.grid(row=9, column=0, columnspan=2, rowspan=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))


        self.GraphPlotFlow()
        self.GraphPlotPressure()

        # plotPressureFrame = Frame(self, bg='green')
        # plotPressureFrame.grid(row=6, column=2, columnspan=3, rowspan=5, sticky=N+S+E+W)
    

        for i in range(0, 11):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)

        # self.GraphPlotFlow()
        # self.GraphPlotPressure()

