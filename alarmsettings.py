import tkinter as tk
from tkinter import StringVar, Button, Tk, font
from tkinter import ttk

def AlarmPop(self, settings):
        popup = Tk()
        popup.attributes('-fullscreen', True)
        popup.wm_title("Alarm settings")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select Alarm values", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)
        
        print("PEEP\n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        
        btn1_text = StringVar()
        btn1_text.set("PEEP\n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        btn1 = Button(popup, textvariable=btn1_text,background='#263655',foreground='white',command=lambda: PeepAlarm(self, settings))
        btn1.config(height=15, width=15, state="normal")
        btn1.pack(side="left", expand = True) 

        btn2_text = StringVar()
        btn2_text.set("Pressure\n\n"+"Max value: "+str(settings.max_pressure)+"\nMin value: "+str(settings.min_pressure))
        btn2 = Button(popup, textvariable=btn2_text,background='#263655',foreground='white', command=lambda: PressureAlarm(self, settings))
        btn2.config(height=15, width=15, state="normal")
        btn2.pack(side="left", expand = True)

        btn3_text = StringVar()
        btn3_text.set("Tidal Volume\n\n"+"Max value: "+str(settings.max_tv)+"\nMin value: "+str(settings.min_tv))
        btn3 = Button(popup, textvariable=btn3_text ,background='#263655',foreground='white', command=lambda: TvAlarm(self, settings))
        btn3.config(height=15, width=15, state="normal")
        btn3.pack(side="left", expand = True)

        btn4_text = StringVar()
        btn4_text.set("Oxygen\n\n"+"Max value: "+str(settings.max_fio2)+"\nMin value: "+str(settings.min_fio2))
        btn4 = Button(popup, textvariable=btn4_text, background='#263655',foreground='white', command=lambda: OxygenAlarm(self, settings))
        btn4.config(height=15, width=15, state="normal")
        btn4.pack(side="left", expand = True)
        
        btn5 = Button(popup, text="Exit",background='#263655',foreground='white', command=lambda: close(popup))
        btn5.config(height=15, width=15, state="normal")
        btn5.pack(side="left", expand = True)
        
        popup.mainloop()
        return
    
def PeepAlarm(self, settings):
    return

def close(popup):
    popup.destroy()
    return

def PressureAlarm(self, settings):
    return

def TvAlarm(self, settings):
    return

def OxygenAlarm(self, settings):
    return