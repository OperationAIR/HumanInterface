# import tkinter as tk
from tkinter import Canvas
from utils.config import ConfigValues

class CurrentValueCanvas(Canvas):

    def __init__(self, parent, title, value, textColor=None):
        Canvas.__init__(self, parent, bd=-2, width=0, height=0)

        self.config = ConfigValues()

        if textColor:
            self.textColor = textColor
        else:
            self.textColor = self.config.values['colors']['green']

        self.text = None

        self.setBackgroundColor(self.config.values['colors']['darkBlue'])
        self.setText(title, value)

    def setBackgroundColor(self, color):
        self.configure(bg=color)

    def setText(self, title, value):
        self.delete("all")

        if isinstance(value, float) or isinstance(value, int):
            self.text = title + '\n' + str(round(value))
        elif isinstance(value, list):
            self.text = title + '\n' + str(round(value[0])) + ' / ' + str(round(value[1])) 

        self.textId = self.create_text(0, 0, anchor="nw", fill=self.textColor,font="HelveticaNeue 13",
                        text=self.text)
    


