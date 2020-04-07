import tkinter as tk
from tkinter import StringVar, Button, Tk
from tkinter import ttk

def alarm_overview(self, settings):
    popup = Tk()
    popup.attributes('-fullscreen', True)
    popup.wm_title("Alarm settings")
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)


    btn1_text = StringVar(popup)
    btn1 = Button(popup, text="Stop",background=BUTTON_COLOR,foreground='white',command=lambda: close(popup))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="bottom", expand = False)


    popup.mainloop()
    return



def close(popup):
    popup.destroy()
    return