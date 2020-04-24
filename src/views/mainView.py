from enum import Enum
from collections import deque
from tkinter import E, Frame, N, S, W

from controllers.alarmController import AlarmController, AlarmType
from models.mcuSensorModel import UPSStatus
from utils.config import ConfigValues
from utils.currentValueCanvas import CurrentValueCanvas
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization
from views.graphView import GraphView


class MainViewActions(Enum):
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
    INSP_HOLD_START = 12
    INSP_HOLD_STOP = 13
    EXP_HOLD_START = 14
    EXP_HOLD_STOP = 15

class MainView(Frame):

    def __init__(self, width, height, settings, sensordata, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, width=width, height=height, bg=self.config.values['colors']['darkBlue'])
        self.settings = settings
        self.sensordata = sensordata
        self.callback = callback

        self.pressureQueue = deque(maxlen=self.config.values['defaultSettings']['pressureQueueLen'])

        self.alarms = AlarmController()

        Internationalization()

        self.fill_frame()

    def getBtnColor(self, low_alarm, high_alarm):
        if self.alarms.hasActiveAlarm(low_alarm) or self.alarms.hasActiveAlarm(high_alarm):
            return self.config.values['colors']['alarmColor']
        return self.config.values['colors']['lightBlue']

    def getCanvasColor(self, *args):
        if any(self.alarms.hasActiveAlarm(arg) is True for arg in args):
            return self.config.values['colors']['alarmColor']
        return self.config.values['colors']['darkBlue']


    def update(self, settings, sensordata):
        self.settings = settings
        self.sensordata = sensordata

        if not self.oxy_btn:
            return

        start_stop_text = ""
        if self.settings.start:
            self.switch_btn.timeout = 4
            self.switch_btn.checkTimeout()
            start_stop_text = _("STOP")
        else:
            self.switch_btn.timeout = 0
            start_stop_text = _("START")

        if self.alarms.present():
            self.alarm_overview_btn.setBackground(self.config.values['colors']['alarmColor'])
        else:
            self.alarm_overview_btn.setBackground()

        self.pressureQueue.append(self.sensordata.pressure)

        self.switch_btn.setText(start_stop_text)
        self.peep_btn.setText(_("PEEP") + '\n' + str(self.settings.peep) + " " + _("[cm H2O]"))
        self.peep_btn.setBackground(self.getBtnColor(AlarmType.PEEP_TOO_LOW, AlarmType.PEEP_TOO_HIGH))
        self.freq_btn.setText(_("Frequency") + '\n' + str(self.settings.freq) + " " + _("[1/min]"))
        self.pres_btn.setText(_("PC above PEEP") + '\n' + str(self.settings.pressure) + " " + _("[cm H2O]"))
        self.pres_btn.setBackground(self.getBtnColor(AlarmType.PRESSURE_TOO_LOW, AlarmType.PRESSURE_TOO_HIGH))
        self.oxy_btn.setText(_("Oxygen (O2)") + '\n' + str(self.settings.oxygen) + " [%]")
        self.oxy_btn.setBackground(self.getBtnColor(AlarmType.OXYGEN_TOO_LOW, AlarmType.OXYGEN_TOO_HIGH))

        self.inspHold_btn.setEnabled(settings.start)
        if sensordata.inspiratory_hold_result:
            self.inspHold_btn.setText(_("Inspiration Hold") + "\n{0:.2g} ".format(sensordata.inspiratory_hold_result) + _("[cm H2O]"))
        self.expHold_btn.setEnabled(settings.start)
        if sensordata.expiratory_hold_result:
            self.expHold_btn.setText(_("Expiration Hold") + "\n{0:.2g} ".format(sensordata.expiratory_hold_result) + _("[cm H2O]"))

        ppeak = max(self.pressureQueue)
        pmean = sum(self.pressureQueue)/len(self.pressureQueue)
        self.ppeak_label.setText(_("Ppeak") + "\n" + _("[cm H2O]"), [ppeak, pmean])

        ppeep = min(self.pressureQueue)
        self.pmean_label.setText(_("Ppeep") + "\n" + _("[cm H2O]"), ppeep)
        self.oxy_label.setText(_("O2") + " [%]", self.sensordata.oxygen)
        self.tvinexp_label.setText(_("TV in/exp") + " \n" + _("[mL]"), str(self.sensordata.tidal_volume_inhale) + "/" + str(self.sensordata.tidal_volume_exhale))
        self.tv_label1.setText(_("min.vol."), str(round(self.sensordata.minute_volume)) + " " + _("[L]"))

        batt_status = self.sensordata.ups_status
        
        if batt_status == (UPSStatus.UNKNOWN or UPSStatus.FAIL):
            self.batt_label.setTitle(_("Pwr. Err."))
        else:
            self.batt_label.setTitle("")

        self.batt_label.setBackgroundColor(self.getCanvasColor(AlarmType.RUN_ON_BATTERY, AlarmType.LOW_BATTERY))

        self.flowgraph.update(-1 * self.sensordata.flow)
        self.pressuregraph.update(self.sensordata.pressure)

    def getFrame(self):
        return self.frame


    def drawGraphs(self):


        # Parameters
        pressure_x_len = 150         # Number of points to display
        pressure_y_range = [0, 40]  # Range of possible Y values to display

        self.pressuregraph = GraphView(_("Pressure"), _("[cm H2O]"), self.sensordata.pressure, pressure_y_range, pressure_x_len, self.config.values['colors']['pressurePlot'], self)
        self.pressuregraph.getPlot().grid(row=1, column=2, rowspan=4, columnspan=2, sticky=N + S + E + W)

        # Parameters
        flow_x_len = 150         # Number of points to display
        flow_y_range = [-60, 0]  # Range of possible Y values to display

        self.flowgraph = GraphView(_("Flow"), _("[L / min]"), self.sensordata.flow, flow_y_range, flow_x_len, self.config.values['colors']['flowPlot'], self)
        self.flowgraph.getPlot().grid(row=5, column=2, rowspan=4, columnspan=2, sticky=N + S + E + W)


    def fill_frame(self):
        # Buttons on the  top and left
        self.air_btn = FlatButton(self, self.callback, MainViewActions.MENU,
                             self.config.values['colors']['lightBlue'])
        self.air_btn.setText(_("Menu"))
        self.air_btn.grid(row=0, column=0, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_btn = FlatButton(self, self.callback, MainViewActions.ALARM, self.config.values['colors']['lightBlue'])
        self.alarm_btn.setText(_("Alarm"))
        self.alarm_btn.grid(row=0, column=1, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.alarm_overview_btn = FlatButton(self, self.callback, MainViewActions.VIEW_ALARMS, self.config.values['colors']['lightBlue'])
        self.alarm_overview_btn.setText(_("Alarm Overview"))
        self.alarm_overview_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.patient_btn = FlatButton(self, self.callback, MainViewActions.PATIENT, self.config.values['colors']['lightBlue'])
        # self.patient_btn.setText(_("Patient"))
        self.patient_btn.setText("")
        self.patient_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=(0,2), pady=(2, 0))

        self.switch_btn = FlatButton(self, self.callback, MainViewActions.STARTSTOP, self.config.values['colors']['lightBlue'], timeout=4)
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
        self.ppeak_label = CurrentValueCanvas(self, _("Ppeak"), 100, self.config.values['colors']['pressurePlot'])
        self.ppeak_label.grid(row=1, column=4, rowspan=2, sticky=N + S + E + W)

        self.pmean_label = CurrentValueCanvas(self, _("Pmean"), 50, self.config.values['colors']['pressurePlot'])
        self.pmean_label.grid(row=3, column=4, rowspan=2, sticky=N + S + E + W)

        self.oxy_label = CurrentValueCanvas(self, _("O2"), self.sensordata.oxygen, 'white')
        self.oxy_label.grid(row=5, column=4, rowspan=2, sticky=N + S + E + W)

        self.tvinexp_label = CurrentValueCanvas(self, _("TV in/exp"), 0, self.config.values['colors']['green'])
        self.tvinexp_label.grid(row=7, column=4, rowspan=2, sticky=N + S + E + W)

        self.tv_label1 = CurrentValueCanvas(self, _("min.vol"),
                                           [self.sensordata.tidal_volume_inhale, self.sensordata.tidal_volume_exhale],
                                           self.config.values['colors']['green'])
        self.tv_label1.grid(row=9, column=4, rowspan=2, sticky=N + S + E + W)

        self.batt_label = CurrentValueCanvas(self, _("Batt. [%]"), self.sensordata.battery_percentage, 'white')
        self.batt_label.grid(row=11, column=4, rowspan=2, sticky=N + S + E + W)

        # Buttons under graphs
        self.inspHold_btn = FlatButton(self, self.callback, MainViewActions.INSP_HOLD_STOP, self.config.values['colors']['lightBlue'])
        self.inspHold_btn.setCustomPressArgument(MainViewActions.INSP_HOLD_START)
        self.inspHold_btn.setText(_("Inspiration Hold\n(Hold to measure)"))
        self.inspHold_btn.grid(row=10, column=2, columnspan=1, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))

        self.expHold_btn = FlatButton(self, self.callback, MainViewActions.EXP_HOLD_STOP, self.config.values['colors']['lightBlue'])
        self.expHold_btn.setCustomPressArgument(MainViewActions.EXP_HOLD_START)
        self.expHold_btn.setText(_("Expiration Hold\n(Hold to measure)"))
        self.expHold_btn.grid(row=10, column=3, columnspan=1, rowspan=3, sticky=N + S + E + W, padx=(0,2), pady=(2,0))


        self.rowconfigure(0, weight=5)
        for i in range(1, 10):
            self.rowconfigure(i, weight=1)
        for i in range(9, 13):
            self.rowconfigure(i, weight=3)

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=5)
        self.columnconfigure(3, weight=5)
        self.columnconfigure(4, weight=2)

        self.drawGraphs()
