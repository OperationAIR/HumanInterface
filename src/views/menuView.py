
from enum import Enum
from tkinter import E, Frame, Label, N, S, StringVar, W

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization


class MenuViewActions(Enum):
    NONE = 0
    SHUTDOWN = 1
    SELF_TEST = 2


class MenuView(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback

        Internationalization()


    def update(self, settings):
        self.exit_btn.checkTimeout()
        self.exit_btn.setEnabled(not settings.start)

        if settings.start:
            self.exit_btn.setText(_("Shutdown Disabled\n(Stop Ventilator First)"))
        else:
            self.exit_btn.setText(_("Shutdown"))

    def fill_frame(self, settings):
        close_btn = FlatButton(self, self.callback, MenuViewActions.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText(_("Close"))
        close_btn.grid(row=0, column=3, sticky=N + S + E + W, padx=10, pady=20)

        self.exit_btn = FlatButton(self, self.callback, MenuViewActions.SHUTDOWN,
                               self.config.values['colors']['lightBlue'], fontSize=20, timeout=4)
        self.exit_btn.grid(row=2, column=2, columnspan=2, sticky=N + S + E + W, padx=(40,0), pady=40)

        if settings.start:
            self.exit_btn.setEnabled(False)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        for i in range(0, 4):
            self.columnconfigure(i, weight=1)
