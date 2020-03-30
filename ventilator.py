import tkinter as tk
import signal
import time
from types import SimpleNamespace
from threading import Thread
from queue import Queue
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar, Button, Tk

from settings import Settings
from mcu import Microcontroller

BAUDRATE = 115200
# TTY = '/dev/ttyS0'
TTY = '/dev/cu.usbmodemC1DDCDF83'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.settings = Settings(
            peep=20,
            freq=20,
            ratio=2,
            tidal_vol=120,
            pressure=40,
            oxygen = 25,
            max_pressure=45,
            min_pressure=5,
            max_tv=400,
            min_tv=200,
            max_fio2=50,
            min_fio2=20)

        self.BuildGui()
        self.queue = Queue()
        self.mcu = Microcontroller(TTY, BAUDRATE, self.queue)

        self._thread_alive = True
        self.io_thread = Thread(target=self.asyncio)
        self.io_thread.start()
        print(self.req_sensors())



    def setValues(self, settings, popup, valuetype, value, text):
        if valuetype == "peep":
            if value <= 35 and value >= 5:
                settings.peep = value
            text.set("Confirm \n PEEP"+'\n'+str(settings.peep))
            return
        if valuetype == "freq":
            if value <= 35 and value >= 0:
                settings.freq = value
            text.set("Confirm \n Frequency"+'\n'+str(settings.freq))
            return
        if valuetype == "pres":
            if value <= 70 and value >= 30:
                settings.pressure = value
            text.set("Confirm \n Pressure"+'\n'+str(settings.pressure))
            return
        if valuetype == "oxygen":
            if value <= 100 and value >= 20:
                settings.oxygen = value
            text.set("Confirm \n Oxygen"+'\n'+str(settings.oxygen))
            return

        valueTida = 200
        valuePres = 30
        valueO2 = 40
        peep_btn_text.set("PEEP"+'\n'+str(valuePEEP))
        popup.destroy()

    def update_buttons(self):
        self.freq_btn_text.set("Frequency"+'\n'+str(self.settings.freq))
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep))
        self.tv_btn_text.set("Tidal Volume"+'\n'+str(self.settings.tidal_vol))
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure))
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen))

    def FreqPop(self, settings):
        popup = Tk()
        popup.wm_title("Frequency")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Frequency value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Frequency"+'\n'+str(settings.freq))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=5, width=10, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq+5, text))
        btn2.config(height=5, width=10, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq-5, text))
        btn3.config(height=5, width=10, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def PeepPop(self, settings):
        popup = Tk()
        popup.wm_title("Peep")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New PEEP value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Peep"+'\n'+str(settings.peep))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=5, width=10, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"peep", settings.peep+5, text))
        btn2.config(height=5, width=10, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"peep", settings.peep-5, text))
        btn3.config(height=5, width=10, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def PresPop(self, settings):
        popup = Tk()
        popup.wm_title("Pressure")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Pressure value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Pressure"+'\n'+str(settings.pressure))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=5, width=10, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"pres", settings.pressure+5, text))
        btn2.config(height=5, width=10, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"pres", settings.pressure-5, text))
        btn3.config(height=5, width=10, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def O2Pop(self, settings):
        popup = Tk()
        popup.wm_title("Oxygen")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Oxygen percentage value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Oxygen [%]"+'\n'+str(settings.oxygen))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=5, width=10, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"oxygen", settings.oxygen+5, text))
        btn2.config(height=5, width=10, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"oxygen", settings.oxygen-5, text))
        btn3.config(height=5, width=10, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return


    def BuildGui(self):
        self.configure(bg= '#161E2E')
        style = ttk.Style()
        style.configure("style.TButton",background='#263655')
        ttk.Style().configure("TButton", padding=6, relief="flat",background='#263655',foreground='#FFFFFF')

        #define grid sizes and frames
        f1 = ttk.Frame(self, width=160, height=60, borderwidth=2)
        f2 = ttk.Frame(self, width=60, height=60, borderwidth=2)
        f3 = ttk.Frame(self, width=340, height=60, borderwidth=2)
        f4 = ttk.Frame(self, width=120, height=60, borderwidth=2)
        f5 = ttk.Frame(self, width=120, height=60, borderwidth=2)
        f6 = ttk.Frame(self, width=160, height=84, borderwidth=2)
        f7 = ttk.Frame(self, width=160, height=84, borderwidth=2)
        #f8 = ttk.Frame(self, width=60, height=188, borderwidth=2)
        #f9 = ttk.Frame(self, width=580, height=210, borderwidth=2)
        f10 = ttk.Frame(self, width=220, height=84, borderwidth=2)
        f11 = ttk.Frame(self, width=220, height=84, borderwidth=2)
        f12 = ttk.Frame(self, width=220, height=84, borderwidth=2)
        #f13 = ttk.Frame(self, width=580, height=210, borderwidth=2)

        f1.grid(row=0, column=0)
        f2.grid(row=0, column=1)
        f3.grid(row=0, column=2)
        f4.grid(row=0, column=3)
        f5.grid(row=0, column=5)
        f6.grid(row=1, column=0)
        f7.grid(row=2, column=0)
        #f8.grid(row=1, column=1,rowspan=2)
        #f9.grid(row=1, column=2, columnspan=3, rowspan=3)
        f10.grid(row=3, column=0, columnspan=2)
        f11.grid(row=4, column=0, columnspan=2)
        f12.grid(row=5, column=0, columnspan=2)
        #f13.grid(row=3, column=1, columnspan=3, rowspan=3)


        air_btn_text = StringVar()
        air_btn_text.set("OperationAir")
        air_btn = Button(f1, textvariable=air_btn_text,background='#263655',foreground='white')
        air_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.alarm_btn_text = StringVar()
        self.alarm_btn_text.set("Alarm")
        self.alarm_btn = Button(f2, textvariable=self.alarm_btn_text,background='#263655',foreground='white')
        self.alarm_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.alarm_name_btn_text = StringVar()
        self.alarm_name_btn_text.set("No alarms")
        self.alarm_name_btn = Button(f3, textvariable=self.alarm_name_btn_text,background='#263655',foreground='white')
        self.alarm_name_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.patient_btn_text = StringVar()
        self.patient_btn_text.set("Patient")
        self.patient_btn = Button(f4, textvariable=self.patient_btn_text,background='#263655',foreground='white' )
        self.patient_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.switch_btn_text = StringVar()
        self.switch_btn_text.set("Started")
        self.switch_btn = Button(f5, textvariable=self.switch_btn_text,background='#263655',foreground='white',command = lambda: self.quit())
        self.switch_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.freq_btn_text = StringVar()
        self.freq_btn_text.set("Frequency"+'\n'+str(self.settings.freq))
        self.freq_btn = Button(f7, textvariable=self.freq_btn_text,background='#263655',foreground='white',command = lambda: self.FreqPop(self.settings))
        self.freq_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.peep_btn_text = StringVar()
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep))
        self.peep_btn = Button(f6, textvariable=self.peep_btn_text,background='#263655',foreground='white',command = lambda: self.PeepPop(self.settings))
        self.peep_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.tv_btn_text = StringVar()
        self.tv_btn_text.set("Tidal Volume"+'\n'+str(self.settings.tidal_vol))
        self.tv_btn = Button(f10, textvariable=self.tv_btn_text,background='#263655',foreground='white')
        self.tv_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.pres_btn_text = StringVar()
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure))
        self.pres_btn = Button(f11, textvariable=self.pres_btn_text,background='#263655',foreground='white',command = lambda: self.PresPop(self.settings) )
        self.pres_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.oxy_btn_text = StringVar()
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen))
        self.oxy_btn = Button(f12, textvariable=self.oxy_btn_text,background='#263655',foreground='white', command = lambda: self.O2Pop(self.settings) )
        self.oxy_btn.place(x=0, y=0, relwidth=1,relheight=1)


    def quit(self, _signal=None, _=None):
        self._thread_alive = False
        self.mcu.disconnect()
        if self.io_thread:
            self.io_thread.join()
        print('bye')
        self.destroy()

    def say_hello(self):
        print("Hello, Tkinter!")
        self.mcu.led_on()

    def say_bye(self):
        print("Bye, Tkinter!")
        self.mcu.led_off()

    def req_sensors(self):
        print('request sensor data')
        self.mcu.request_sensor_data()

    def send_settings(self, popup):
        self.mcu.send_settings(self.settings)
        self.update_buttons()
        popup.destroy()
        print("Send settings")

    def asyncio(self):
        while self._thread_alive:

            if not self.queue.empty():
                packet = self.queue.get()
                print("Got packet:")
                print(packet)

            time.sleep(0.1)



if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.title("Operation Air Ventilator")
    app.geometry('800x480')
    signal.signal(signal.SIGINT, app.quit)
    app.attributes('-fullscreen', True)
    app.mainloop()
