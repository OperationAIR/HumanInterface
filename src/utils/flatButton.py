import tkinter as tk
from tkinter import Canvas
from utils.config import ConfigValues

class FlatButton(Canvas):

    def __init__(self, parent, callback, arg=None, color=None, pressColor=None, fontSize=None):
        Canvas.__init__(self, parent, width=0, height=0, bd=-2, bg=color, highlightthickness=0, relief='ridge')
        self.textColor = "White"
        self.textId = None

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
        self.bind("<Button-1>", self.pressEvent)
        self.bind("<ButtonRelease-1>", self.releaseEvent)
        self.bind("<Configure>", self.centerText)

    def pressEvent(self, event):
        if self.callback:
            self.configure(bg=self.pressColor)

    def releaseEvent(self, event):
        self.configure(bg=self.color)
        if self.callback:
            self.callback(self.arg)

    def centerText(self, event):
        self.delete(self.textId)
        self.textId = self.create_text(0, 0, anchor="nw", fill=self.textColor,font="HelveticaNeue " + str(self.fontSize),
                        text=self.text)
        xOffset = self.findXCenter(self.textId)
        yOffset = self.findYCenter(self.textId)
        self.move(self.textId, xOffset, yOffset)

    def findXCenter(self, item):
        coords = self.bbox(item)
        xOffset = (self.winfo_width() / 2) - ((coords[2] - coords[0]) / 2)
        return xOffset

    def findYCenter(self, item):
        coords = self.bbox(item)
        yOffset = (self.winfo_height()/ 2) - ((coords[3] - coords[1]) / 2)
        return yOffset

    def setText(self, text, color=None):
        self.text = text
        if color:
            self.textColor = color

        self.delete(self.textId)
        self.centerText(None)
