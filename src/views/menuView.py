
from enum import Enum
from tkinter import E, Frame, Label, N, S, StringVar, W

from utils.config import ConfigValues
from utils.flatButton import FlatButton
from utils.internationalization import Internationalization


class MenuViewActions(Enum):
    NONE = 0
    SHUTDOWN = 1
    SELF_TEST = 2
    INSPIRATORY_HOLD_START = 3
    INSPIRATORY_HOLD_STOP = 4
    EXPIRATORY_HOLD_START = 5
    EXPIRATORY_HOLD_STOP = 6


class MenuView(Frame):

    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback

        Internationalization()

    def fill_frame(self):
        print("Filling frame!")
        close_btn = FlatButton(self, self.callback, MenuViewActions.NONE,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        close_btn.setText(_("Close"))
        close_btn.grid(row=0, column=2, sticky=N + S + E + W, padx=10, pady=20)

        exit_btn = FlatButton(self, self.callback, MenuViewActions.SHUTDOWN,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        exit_btn.setText(_("Shutdown"))
        exit_btn.grid(row=1, column=2, sticky=N + S + E + W, padx=(40,0), pady=40)


        test_btn = FlatButton(self, self.callback, MenuViewActions.SELF_TEST,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        test_btn.setText(_("Self Test"))
        test_btn.grid(row=1, column=0, sticky=N + S + E + W,padx=(1,0), pady=40)

        insp_hold_btn = FlatButton(self, self.callback, MenuViewActions.INSPIRATORY_HOLD_START,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        insp_hold_btn.setText(_("Inspiratory\nHold"))
        insp_hold_btn.grid(row=2, column=0, sticky=N + S + E + W,padx=(1,0), pady=40)

        insp_hold_stop_btn = FlatButton(self, self.callback, MenuViewActions.INSPIRATORY_HOLD_STOP,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        insp_hold_stop_btn.setText(_("Stop Insp.\nHold"))
        insp_hold_stop_btn.grid(row=2, column=1, sticky=N + S + E + W,padx=(1,0), pady=40)

        self.insp_hold_text = StringVar()

        insp_hold_label = Label(self, textvariable=self.insp_hold_text)
        self.insp_hold_text.set("Insp hold: xx")
        insp_hold_label.grid(row=2, column=2, sticky=N + S + E + W,padx=(1,0), pady=40)



        exp_hold_btn = FlatButton(self, self.callback, MenuViewActions.EXPIRATORY_HOLD_START,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        exp_hold_btn.setText(_("Expiratory\nHold"))
        exp_hold_btn.grid(row=3, column=0, sticky=N + S + E + W,padx=(1,0), pady=40)

        exp_hold_stop_btn = FlatButton(self, self.callback, MenuViewActions.EXPIRATORY_HOLD_STOP,
                               self.config.values['colors']['lightBlue'], fontSize=20)
        exp_hold_stop_btn.setText(_("Stop Exp.\nHold"))
        exp_hold_stop_btn.grid(row=3, column=1, sticky=N + S + E + W,padx=(1,0), pady=40)

        self.exp_hold_text = StringVar()

        exp_hold_label = Label(self, textvariable=self.exp_hold_text)
        self.exp_hold_text.set("exp hold: xx")
        exp_hold_label.grid(row=3, column=2, sticky=N + S + E + W,padx=(1,0), pady=40)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=2)

        for i in range(0, 3):
            self.columnconfigure(i, weight=1)

    def update(self, insp_hold_value, exp_hold_value):
        self.insp_hold_text.set('{0:.2g} [cm H2O]'.format(insp_hold_value))
        self.exp_hold_text.set('{0:.2g} [cm H2O]'.format(exp_hold_value))
