from tkinter import E, Frame, N, S, W

from utils.config import ConfigValues
from utils.constants import SettingType
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization


class AlarmSettingsOverview(Frame):

    def __init__(self, settings, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback
        self.settings = settings

        Internationalization()


    def fill_frame(self):
        close_btn = FlatButton(self, self.callback, None,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText(_("Close"))
        close_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=10)

        peep_btn = FlatButton(self, self.callback, SettingType.PEEP,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        peep_btn.setText(_("PEEP") + "\n" + str(self.settings.min_peep) + "-" + str(self.settings.max_peep))
        peep_btn.grid(row=1, column=0, sticky=N + S + E + W, padx=(40,0), pady=80)

        press_btn = FlatButton(self, self.callback, SettingType.PRESSURE,
                   self.config.values['colors']['lightBlue'], fontSize=20)
        press_btn.setText(_("Pressure") + "\n" + str(self.settings.min_pressure) + "-" + str(self.settings.max_pressure))
        press_btn.grid(row=1, column=1, sticky=N + S + E + W,padx=(2,0), pady=80)

        tidal_btn = FlatButton(self, self.callback, SettingType.TIDAL,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        tidal_btn.setText(_("Tidal Volume") + "\n" + str(self.settings.min_tv) + "-" + str(self.settings.max_tv))
        tidal_btn.grid(row=1, column=2, sticky=N + S + E + W,padx=(2,0), pady=80)

        oxy_btn = FlatButton(self, self.callback, SettingType.OXYGEN,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        oxy_btn.setText(_("Oxygen") + "\n" + str(self.settings.min_fio2) + "-" + str(self.settings.max_fio2))
        oxy_btn.grid(row=1, column=3, sticky=N + S + E + W,padx=(2,40), pady=80)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)
