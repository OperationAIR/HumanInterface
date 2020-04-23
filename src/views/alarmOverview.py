from tkinter import E, Frame, N, S, W

from controllers.alarmController import AlarmController, AlarmType
from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization


class AlarmOverview(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        Internationalization()

        self.callback = callback
        self.alarms = AlarmController()

        self.alarm_btns = []

    def fill_frame(self):
        for btn in self.alarm_btns:
            btn.destroy()

        self.alarm_btns.clear()

        clear_btn = FlatButton(self, self.callback, AlarmType.CLEAR,
                             self.config.values['colors']['lightBlue'], fontSize=15)
        clear_btn.setText(_("Clear\nInactive Alarms"))
        clear_btn.grid(row=0, column=0, sticky=N + S + E + W, padx=10, pady=10)

        close_btn = FlatButton(self, self.callback, AlarmType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText(_("Close"))
        close_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=10)

        for i in range(0, len(self.alarms.alarms)):
            color = self.config.values['colors']['lightBlue']
            if self.alarms.alarms[i].active:
                color = self.config.values['colors']['alarmColor']
                
            if self.alarms.alarms[i].type == AlarmType.RUN_ON_BATTERY:
                self.alarm_btns.append(FlatButton(self, self.callback, self.alarms.alarms[i].type,
                    color, fontSize=20, pressable=False))
            else:
                self.alarm_btns.append(FlatButton(self, self.callback, self.alarms.alarms[i].type,
                    color, fontSize=20))

            self.alarm_btns[i].setText(self.alarms.alarms[i])
            self.alarm_btns[i].grid(row=i + 1, column=0, columnspan=4, sticky=N + S + E + W, padx=10, pady=10)

        for i in range(0, len(self.alarms.alarms) + 1):
            self.rowconfigure(i, weight=1)
        for i in range(0, 4):
            self.columnconfigure(i, weight=1)
