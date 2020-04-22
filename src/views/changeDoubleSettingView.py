from enum import Enum
from tkinter import E, Frame, N, S, W

from utils.config import ConfigValues
from utils.constants import SettingType
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization


class ChangeAlarmViewActions(Enum):
    CONFIRM = 2
    MINMINUS = 3
    MINPLUS = 4
    MAXMINUS = 5
    MAXPLUS = 6

class ChangeDoubleSettingView(Frame):
    Internationalization()

    # bound (Bool): Are the two variables linked? (Can variable 2 be less than variable 1)
    def __init__(self, stype, min_current, min_min, min_max, step1, max_current, max_min, max_max, step2, description, callback, label1=_("Minimum\nValue"), label2=_("Maximum\nValue"), bound=True, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.type = stype

        self.bound = bound
        self.step1 = step1
        self.label1 = label1
        self.min_current = min_current
        self.min_min = min_min
        self.min_max = min_max

        self.label2 = label2
        self.step2 = step2
        self.max_current = max_current
        self.max_min = max_min
        self.max_max = max_max
        self.description = description
        self.callback = callback

        self.fill_frame()

    def confirmSetting(self, stype):
        self.callback(stype, self.min_current, self.max_current)

    def valueChange(self, action):
        if action == ChangeAlarmViewActions.MINMINUS:
            if self.min_current - self.step1 >= self.min_min:
                if self.min_current % self.step1 != 0:
                    self.min_current = self.min_current - (self.min_current % self.step1)
                else:
                    self.min_current = self.min_current - self.step1
            else:
                self.min_current = self.min_min

        elif action == ChangeAlarmViewActions.MINPLUS:
            if (not self.bound or self.max_current - self.min_current > self.step1):
                if self.min_current + self.step1 <= self.min_max:
                    self.min_current = self.min_current + self.step1 - (self.min_current % self.step1)

        elif action == ChangeAlarmViewActions.MAXMINUS and self.max_current - self.step2 >= self.max_min and (not self.bound or self.max_current - self.min_current > self.step2):
            if self.max_current % self.step2 != 0:
                self.max_current = self.max_current - (self.max_current % self.step2)
            else:
                self.max_current = self.max_current - self.step2

        elif action == ChangeAlarmViewActions.MAXPLUS:
            if self.max_current + self.step2 <= self.max_max:
                self.max_current = self.max_current + self.step2 - (self.max_current % self.step2)
            else:
                self.max_current = self.max_max

        self.min_value_btn.setText(self.min_current)
        self.max_value_btn.setText(self.max_current)

    def fill_frame(self):

        pad = 1

        desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        desc_btn.setText(self.description)
        desc_btn.grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)

        close_btn = FlatButton(self, self.confirmSetting, SettingType.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText(_("Close"))
        close_btn.grid(row=0, column=3, sticky=N+S+E+W, padx=10, pady=10)

        min_desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=20)
        min_desc_btn.setText(self.label1)
        min_desc_btn.grid(row=1, column=0, sticky=N + S + E + W)

        minminus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MINMINUS,
                                  self.config.values['colors']['lightBlue'], fontSize=30)
        minminus_btn.setText("-")
        minminus_btn.grid(row=1, column=1, sticky=N + S + E + W, padx=pad, pady=pad)

        minplus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MINPLUS,
                                 self.config.values['colors']['lightBlue'], fontSize=30)
        minplus_btn.setText("+")
        minplus_btn.grid(row=1, column=2, sticky=N + S + E + W, padx=pad, pady=pad)

        self.min_value_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        self.min_value_btn.setText(self.min_current)
        self.min_value_btn.grid(row=1, column=3, sticky=N + S + E + W)

        max_desc_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=20)
        max_desc_btn.setText(self.label2)
        max_desc_btn.grid(row=2, column=0, sticky=N + S + E + W)

        maxminus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MAXMINUS,
                                  self.config.values['colors']['lightBlue'], fontSize=30)
        maxminus_btn.setText("-")
        maxminus_btn.grid(row=2, column=1, sticky=N + S + E + W,padx=pad, pady=pad)

        maxplus_btn = FlatButton(self, self.valueChange, ChangeAlarmViewActions.MAXPLUS,
                                 self.config.values['colors']['lightBlue'], fontSize=30)
        maxplus_btn.setText("+")
        maxplus_btn.grid(row=2, column=2, sticky=N + S + E + W,padx=pad, pady=pad)

        self.max_value_btn = FlatButton(self, None, None,
                                  self.config.values['colors']['darkBlue'], fontSize=30)
        self.max_value_btn.setText(self.max_current)
        self.max_value_btn.grid(row=2, column=3, sticky=N + S + E + W)

        confirm_btn = FlatButton(self, self.confirmSetting, self.type, self.config.values['colors']['green'], fontSize=40)
        confirm_btn.setText(_("Confirm"), "white")
        confirm_btn.grid(row=3, column=0, columnspan=4, sticky=N + S + E + W, padx=20, pady=(60, 20))

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)
        for i in range(1, 4):
            self.rowconfigure(i, weight=2)
