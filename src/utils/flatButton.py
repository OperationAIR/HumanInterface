from time import time
from tkinter import Canvas
import math

from utils.config import ConfigValues
from utils.internationalization import Internationalization


class FlatButton(Canvas):

    def __init__(self, parent, callback, arg=None, color=None, pressColor=None, fontSize=None, timeout=None, pressable=True):
        Canvas.__init__(self, parent, width=0, height=0, bd=-2, bg=color, highlightthickness=0, relief='ridge')

        Internationalization()

        self.config = ConfigValues()
        self.color = color
        if pressColor:
            self.pressColor = pressColor
        else:
            self.pressColor = self.config.values['colors']['mediumBlue']


        self.callback = callback
        self.arg = arg

        if fontSize:
            self.fontSize = fontSize
        else:
            self.fontSize = 13

        self.textColor = "White"
        self.text = ""
        self.oldText = ""
        self.bind("<Button-1>", self.pressEvent)
        self.bind("<ButtonRelease-1>", self.releaseEvent)
        self.bind("<Configure>", self.centerText)
        self.timeout = 0

        if timeout:
            self.timeout = timeout

        self.timestamp = time()
        self.time_diff = 0
        self.counting = False
        self.press_arg = None

        self.pressable = pressable

        self.enabled = True

    def checkTimeout(self):
        if self.counting:
            self.time_diff = time() - self.timestamp
            if self.time_diff > self.timeout and self.oldText != "":
                self.setText(self.oldText)
                self.text = self.oldText
                self.oldText = ""
                self.callback(self.arg)
            else:
                self.text = _("Hold for") + "\n" + str(math.ceil(self.timeout - self.time_diff)) + " s"
                self.setText(self.text)
            return

    def setEnabled(self, state):
        if state == self.enabled:
            return
        self.enabled = state
        if not self.enabled:
            self.configure(bg=self.pressColor)
        else:
            self.configure(bg=self.color)

    def pressEvent(self, event):
        if not self.pressable:
            return

        if self.timeout > 0 and self.enabled:
            self.timestamp = time()
            self.oldText = self.text
            self.text = _("Hold for") + "\n" + str(self.timeout) + " s"
            self.setText(self.text)
            self.counting = True

        if self.callback and self.enabled:
            self.configure(bg=self.pressColor)
            if self.press_arg:
                self.callback(self.press_arg)

    def setCustomPressArgument(self, press_arg):
        self.press_arg = press_arg

    def releaseEvent(self, event):
        if not self.pressable:
            return

        if self.enabled:
            self.configure(bg=self.color)

        if self.counting:
            self.counting = False
            self.setText(self.oldText)
            self.text = self.oldText
            self.oldText = ""

        elif self.callback and self.enabled:
            arg = self.arg
            self.callback(arg)

    def setBackground(self, color=None):
        if not color:
            color = self.color
        self.configure(bg=color)

    def centerText(self, event):
        self.delete("all")
        self.textId = self.create_text(0, 0, anchor="nw", fill=self.textColor,font="HelveticaNeue " + str(self.fontSize),
                        text=self.text)
        xOffset = self.findXCenter(self.textId)
        yOffset = self.findYCenter(self.textId)
        self.move(self.textId, xOffset, yOffset)

    def findXCenter(self, item):
        coords = self.bbox(item)
        if coords is not None:
            xOffset = (self.winfo_width() / 2) - ((coords[2] - coords[0]) / 2)
            return xOffset
        return 0

    def findYCenter(self, item):
        coords = self.bbox(item)
        if coords is not None:
            yOffset = (self.winfo_height()/ 2) - ((coords[3] - coords[1]) / 2)
            return yOffset
        return 0

    def setText(self, text, color=None):
        if self.oldText == text:
            return

        self.text = text
        if color:
            self.textColor = color

        self.centerText(None)
