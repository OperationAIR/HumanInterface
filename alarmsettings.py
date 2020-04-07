import tkinter as tk
from tkinter import StringVar, Button, Tk, font
from tkinter import ttk
from constants import *

def AlarmPop(self, settings):
    popup = Tk()
    popup.attributes('-fullscreen', True)
    popup.wm_title("Alarm settings")
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)
    label1 = ttk.Label(popup, text="Select Alarm values", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    btn1_text = StringVar(popup)
    btn1_text.set("PEEP\n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
    btn1 = Button(popup, textvariable=btn1_text,background=BUTTON_COLOR,foreground='white',command=lambda: PeepAlarm(self, settings, btn1_text))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="left", expand = True)

    btn2_text = StringVar(popup)
    btn2_text.set("Pressure\n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
    btn2 = Button(popup, textvariable=btn2_text,background=BUTTON_COLOR,foreground='white', command=lambda: PressureAlarm(self, settings, btn2_text))
    btn2.config(height=15, width=15, state="normal")
    btn2.pack(side="left", expand = True)

    btn3_text = StringVar(popup)
    btn3_text.set("Tidal Volume\n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
    btn3 = Button(popup, textvariable=btn3_text ,background=BUTTON_COLOR,foreground='white', command=lambda: TvAlarm(self, settings, btn3_text))
    btn3.config(height=15, width=15, state="normal")
    btn3.pack(side="left", expand = True)

    btn4_text = StringVar(popup)
    btn4_text.set("Oxygen\n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
    btn4 = Button(popup, textvariable=btn4_text, background=BUTTON_COLOR,foreground='white', command=lambda: OxygenAlarm(self, settings, btn4_text))
    btn4.config(height=15, width=15, state="normal")
    btn4.pack(side="left", expand = True)

    btn5 = Button(popup, text="Exit",background=BUTTON_COLOR,foreground='white', command=lambda: close(popup))
    btn5.config(height=15, width=15, state="normal")
    btn5.pack(side="left", expand = True)

    popup.mainloop()
    return

def PeepAlarm(self, settings, text1):
    popup = Tk()
    popup.wm_title("PEEP Alarm")
    popup.attributes('-fullscreen', True)
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)
    label1 = ttk.Label(popup, text="Select New PEEP Alarm", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    text2 = StringVar(popup)
    text2.set("PEEP\n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
    text_btn = Button(popup, textvariable=text2,background=BUTTON_COLOR,foreground='white',command=lambda: close(popup))
    text_btn.config(height=15, width=15, state="normal")
    text_btn.pack(side="left", expand = True)

    btn1 = Button(popup, text="+ MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxPeep", settings.max_peep+5, text1, text2))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="left",expand = True)

    btn2 = Button(popup, text="- MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxPeep", settings.max_peep-5, text1, text2))
    btn2.config(height=15, width=15, state="normal")
    btn2.pack(side="left",expand = True)

    btn3 = Button(popup, text="+ MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinPeep", settings.min_peep+5, text1, text2))
    btn3.config(height=15, width=15, state="normal")
    btn3.pack(side="left",expand = True)

    btn4 = Button(popup, text="- MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinPeep", settings.min_peep-5, text1, text2))
    btn4.config(height=15, width=15, state="normal")
    btn4.pack(side="left",expand = True)

    popup.mainloop()
    return

def TvAlarm(self, settings, text1):
    popup = Tk()
    popup.wm_title("TV Alarm")
    popup.attributes('-fullscreen', True)
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)
    label1 = ttk.Label(popup, text="Select New TV Alarm", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    text2 = StringVar(popup)
    text2.set("TV\n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
    text_btn = Button(popup, textvariable=text2,background=BUTTON_COLOR,foreground='white',command=lambda: close(popup))
    text_btn.config(height=15, width=15, state="normal")
    text_btn.pack(side="left", expand = True)

    btn1 = Button(popup, text="+ MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxTV", settings.max_tv+50, text1, text2))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="left",expand = True)

    btn2 = Button(popup, text="- MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxTV", settings.max_tv-50, text1, text2))
    btn2.config(height=15, width=15, state="normal")
    btn2.pack(side="left",expand = True)

    btn3 = Button(popup, text="+ MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinTV", settings.min_tv+50, text1, text2))
    btn3.config(height=15, width=15, state="normal")
    btn3.pack(side="left",expand = True)

    btn4 = Button(popup, text="- MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinTV", settings.min_tv-50, text1, text2))
    btn4.config(height=15, width=15, state="normal")
    btn4.pack(side="left",expand = True)

    popup.mainloop()
    return

def OxygenAlarm(self, settings, text1):
    popup = Tk()
    popup.wm_title("O2 Alarm")
    popup.attributes('-fullscreen', True)
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)
    label1 = ttk.Label(popup, text="Select New O2 Alarm", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    text2 = StringVar(popup)
    text2.set("O2\n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
    text_btn = Button(popup, textvariable=text2,background=BUTTON_COLOR,foreground='white',command=lambda: close(popup))
    text_btn.config(height=15, width=15, state="normal")
    text_btn.pack(side="left", expand = True)

    btn1 = Button(popup, text="+ MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"Maxfio2", settings.max_fio2+5, text1, text2))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="left",expand = True)

    btn2 = Button(popup, text="- MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"Maxfio2", settings.max_fio2-5, text1, text2))
    btn2.config(height=15, width=15, state="normal")
    btn2.pack(side="left",expand = True)

    btn3 = Button(popup, text="+ MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"Minfio2", settings.min_fio2+5, text1, text2))
    btn3.config(height=15, width=15, state="normal")
    btn3.pack(side="left",expand = True)

    btn4 = Button(popup, text="- MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"Minfio2", settings.min_fio2-5, text1, text2))
    btn4.config(height=15, width=15, state="normal")
    btn4.pack(side="left",expand = True)

    popup.mainloop()
    return

def PressureAlarm(self, settings, text1):
    popup = Tk()
    popup.wm_title("pressure Alarm")
    popup.attributes('-fullscreen', True)
    popup.geometry(WINDOW_DIMENSIONS)
    popup.configure(bg= BACKGROUND_COLOR)
    label1 = ttk.Label(popup, text="Select New pressure Alarm", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    text2 = StringVar(popup)
    text2.set("pressure\n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
    text_btn = Button(popup, textvariable=text2,background=BUTTON_COLOR,foreground='white',command=lambda: close(popup))
    text_btn.config(height=15, width=15, state="normal")
    text_btn.pack(side="left", expand = True)

    btn1 = Button(popup, text="+ MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxPressure", settings.max_pressure+5, text1, text2))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="left",expand = True)

    btn2 = Button(popup, text="- MAX Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MaxPressure", settings.max_pressure-5, text1, text2))
    btn2.config(height=15, width=15, state="normal")
    btn2.pack(side="left",expand = True)

    btn3 = Button(popup, text="+ MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinPressure", settings.min_pressure+5, text1, text2))
    btn3.config(height=15, width=15, state="normal")
    btn3.pack(side="left",expand = True)

    btn4 = Button(popup, text="- MIN Alarm",background=BUTTON_COLOR,foreground='white', command=lambda: setAlarmValues(self, settings, popup,"MinPressure", settings.min_pressure-5, text1, text2))
    btn4.config(height=15, width=15, state="normal")
    btn4.pack(side="left",expand = True)

    popup.mainloop()
    return

def setAlarmValues(self, settings, popup, valuetype, value, text1, text2):
    if valuetype == "MaxPeep":
        if value > settings.min_peep and value <= 70:
            settings.max_peep = value
        text1.set("PEEP \n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
        return
    if valuetype == "MinPeep":
        if value >= 5 and value < settings.max_peep:
            settings.min_peep = value
        text1.set("PEEP \n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_peep)+"\nMin value: "+str(settings.min_peep))
        return
    if valuetype == "MaxPressure":
        if value > settings.min_pressure and value <= 70:
            settings.max_pressure = value
        text1.set("Pressure \n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        return
    if valuetype == "MinPressure":
        if value >= 5 and value < settings.max_pressure:
            settings.min_pressure = value
        text1.set("Pressure \n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        return
    if valuetype == "MaxTV":
        if value > settings.min_tv and value <= 1000:
            settings.max_tv = value
        text1.set("Tidal Volume \n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
        return
    if valuetype == "MinTV":
        if value >= 50 and value < settings.max_tv:
            settings.min_tv = value
        text1.set("Tidal Volume \n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
        return
    if valuetype == "Maxfio2":
        if value > settings.min_fio2 and value <= 100:
            settings.max_fio2 = value
        text1.set("Oxygen \n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
        return
    if valuetype == "Minfio2":
        if value >= 20 and value < settings.max_fio2:
            settings.min_fio2 = value
        text1.set("Oxygen \n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
        text2.set("Confirm Alarms \n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
        return
    popup.destroy()

def close(popup):
    popup.destroy()
    return