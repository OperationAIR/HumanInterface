from enum import Enum
from datetime import datetime
from tkinter import E, Frame, N, S, W

from utils.config import ConfigValues
from utils.flatButton import FlatButton

from utils.internationalization import Internationalization


class SetTimeCallback(Enum):
    CLOSE = 0
    SET_TIME = 1

class SetTimeView(Frame):

    # bound (Bool): Are the two variables linked? (Can variable 2 be less than variable 1)
    def __init__(self, callback, parent=None):
        self.config = ConfigValues()
        Frame.__init__(self, parent, bg=self.config.values['colors']['darkBlue'])

        self.callback = callback
        now = datetime.now()
        dt = now.strftime("%H%M")
        self.time = [int(dt[0]), int(dt[1]), int(dt[2]), int(dt[3])]

        Internationalization()

        self.fill_frame()

    def getTime(self):
        return str(self.time[0]) + str(self.time[1]) + ":" + str(self.time[2]) + str(self.time[3])

    def returnTimeCallback(self, ttype):
        self.callback(ttype, self.getTime())

    def makeValid(self, time, index, change):
        if index == 0:
            time[0] += change
            if time[0] == -1 or time[0] == 3:
                time[0] += (-1*change*3)
            if time[0] == 2 and time[1] > 3:
                time[1] = 3

        if index == 1:
            time[1] += change
            if time[0] == 2 and time[1] == 4:
                time[1] = 0
            elif time[1] == -1:
                if time[0] == 2:
                    time[1] = 3
                else:
                    time[1] = 9
            elif time[1] > 9:
                time[1] = 0
                
        if index == 2:
            time[2] += change
            if time[2] in [-1, 6]:
                time[2] += (-1*change*6)
        
        if index == 3:
            time[3] += change
            if time[3] in [-1, 10]:
                time[3] += (-1*change*10)
        

        return time

    def update(self):
        self.first_digit.setText(self.time[0])
        self.second_digit.setText(self.time[1])
        self.third_digit.setText(self.time[2])
        self.fourth_digit.setText(self.time[3])

    def changeTimeCallback(self, arg):
        (index, change) = arg
        newtime = self.time[:]
 
        self.time = self.makeValid(newtime, index, change)

        self.update()

    def drawPlusButtons(self):
        first_plus = FlatButton(self, self.changeTimeCallback, (0, 1), self.config.values['colors']['lightBlue'], fontSize=40)
        first_plus.setText("+")
        first_plus.grid(row=1, column=0, sticky=N+S+E+W, padx=10, pady=10)

        second_plus = FlatButton(self, self.changeTimeCallback, (1, 1), self.config.values['colors']['lightBlue'], fontSize=40)
        second_plus.setText("+")
        second_plus.grid(row=1, column=1, sticky=N+S+E+W, padx=10, pady=10)

        third_plus = FlatButton(self, self.changeTimeCallback, (2, 1), self.config.values['colors']['lightBlue'], fontSize=40)
        third_plus.setText("+")
        third_plus.grid(row=1, column=3, sticky=N+S+E+W, padx=10, pady=10)

        fourth_plus = FlatButton(self, self.changeTimeCallback, (3, 1), self.config.values['colors']['lightBlue'], fontSize=40)
        fourth_plus.setText("+")
        fourth_plus.grid(row=1, column=4, sticky=N+S+E+W, padx=10, pady=10)

    def drawTime(self):
        self.first_digit = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=40)
        self.first_digit.grid(row=2, column=0, sticky=N+S+E+W, padx=10, pady=10)

        self.second_digit = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=40)
        self.second_digit.grid(row=2, column=1, sticky=N + S + E + W, padx=10, pady=10)

        dots = FlatButton(self, self.changeTimeCallback, (1, 1), self.config.values['colors']['darkBlue'],
                                 fontSize=40)
        dots.setText(":")
        dots.grid(row=2, column=2, sticky=N + S + E + W, padx=10, pady=10)

        self.third_digit = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=40)
        self.third_digit.grid(row=2, column=3, sticky=N + S + E + W, padx=10, pady=10)

        self.fourth_digit = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=40)
        self.fourth_digit.grid(row=2, column=4, sticky=N + S + E + W, padx=10, pady=10)

        self.update()

    def drawMinusButtons(self):
        first_miuns = FlatButton(self, self.changeTimeCallback, (0, -1), self.config.values['colors']['lightBlue'], fontSize=40)
        first_miuns.setText("-")
        first_miuns.grid(row=3, column=0, sticky=N+S+E+W, padx=10, pady=10)

        second_miuns = FlatButton(self, self.changeTimeCallback, (1, -1), self.config.values['colors']['lightBlue'], fontSize=40)
        second_miuns.setText("-")
        second_miuns.grid(row=3, column=1, sticky=N+S+E+W, padx=10, pady=10)

        third_miuns = FlatButton(self, self.changeTimeCallback, (2, -1), self.config.values['colors']['lightBlue'], fontSize=40)
        third_miuns.setText("-")
        third_miuns.grid(row=3, column=3, sticky=N+S+E+W, padx=10, pady=10)

        fourth_miuns = FlatButton(self, self.changeTimeCallback, (3, -1), self.config.values['colors']['lightBlue'], fontSize=40)
        fourth_miuns.setText("-")
        fourth_miuns.grid(row=3, column=4, sticky=N+S+E+W, padx=10, pady=10)


    def fill_frame(self):
        label_btn = FlatButton(self, None, None, self.config.values['colors']['darkBlue'], fontSize=25)
        label_btn.setText(_("Set the Time"))
        label_btn.grid(row=0, column=0, columnspan=5, sticky=N+S+E+W, padx=10, pady=10)

        self.drawPlusButtons()
        self.drawTime()
        self.drawMinusButtons()

        confirm_btn = FlatButton(self, self.returnTimeCallback, SetTimeCallback.SET_TIME, self.config.values['colors']['green'], fontSize=40)
        confirm_btn.setText(_("Confirm"), "white")
        confirm_btn.grid(row=4, column=0, columnspan=5, sticky=N + S + E + W, padx=20, pady=(60, 20))

        for i in range(0, 5):
            self.columnconfigure(i, weight=5)

        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        for i in range(1, 5):
            self.rowconfigure(i, weight=2)
