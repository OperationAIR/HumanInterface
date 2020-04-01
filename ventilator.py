import tkinter as tk
import signal
import time
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
from time import sleep
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from types import SimpleNamespace
from threading import Thread
from queue import Queue
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar, Button, Tk, font

from settings import Settings
from sensors import Sensors
from alarmsettings import AlarmPop
from mcu import Microcontroller

import gui_utils as gut

BAUDRATE = 115200

FULLSCREEN = False
SIMULATE = False
# for RPi
#TTY = '/dev/ttyS0'
# for Mac
#TTY = '/dev/cu.usbmodemC1DDCDF83'
# for Ubuntu
TTY = '/dev/ttyUSB0'

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #For plotting
        self.line_pressure = None
        self.line_flow = None
        self.ys_p = []
        self.ys_f = []
        self.pressure_animation_ref = None

        self.latest_sensor_data = Sensors(
            flow=30,
            pressure1=45,
            pressure2=45,
            oxygen=40)

        self.settings = Settings(
            start=0,
            peep=20,
            freq=20,
            ratio=2,
            pressure=40,
            oxygen = 25,
            max_pressure=50,
            min_pressure=40,
            max_tv=400,
            min_tv=200,
            max_fio2=50,
            min_fio2=20,
            max_peep = 35,
            min_peep = 5)
        
        self.BuildGui()
        self.sensor_queue = Queue()
        self.settings_queue = Queue()
        self.mcu = Microcontroller(TTY, BAUDRATE, self.settings_queue, self.sensor_queue, simulate=SIMULATE)

        self._thread_alive = True
        self.io_thread = None
        self.io_thread = Thread(target=self.asyncio)
        self.io_thread.start()
        print(self.req_sensors())

    def giveAlarm(self):
        pass # print("alarm!!")

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
        popup.destroy()

    def update_buttons(self):
        self.freq_btn_text.set("Frequency"+'\n'+str(self.settings.freq)+" [1/min]")
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep)+" [mmHg]")
        #self.tv_btn_text.set("Tidal Volume"+'\n'+str(self.settings.tidal_vol)+" [L/min]")
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure)+" [mmHg]")
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen)+" [%]")

    def FreqPop(self, settings):
        popup = Tk()
        popup.attributes('-fullscreen', True)
        popup.wm_title("Frequency")
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Frequency value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Frequency"+'\n'+str(settings.freq))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=15, width=30, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq+5, text))
        btn2.config(height=15, width=30, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq-5, text))
        btn3.config(height=15, width=30, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def PeepPop(self, settings):
        popup = Tk()
        popup.wm_title("Peep")
        popup.attributes('-fullscreen', True)
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New PEEP value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Peep"+'\n'+str(settings.peep))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=15, width=30, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"peep", settings.peep+5, text))
        btn2.config(height=15, width=30, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"peep", settings.peep-5, text))
        btn3.config(height=15, width=30, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def PresPop(self, settings):
        popup = Tk()
        popup.wm_title("Pressure")
        popup.attributes('-fullscreen', True)
        popup.geometry('800x480')
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Pressure value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Pressure"+'\n'+str(settings.pressure))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=15, width=30, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"pres", settings.pressure+5, text))
        btn2.config(height=15, width=30, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"pres", settings.pressure-5, text))
        btn3.config(height=15, width=30, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def O2Pop(self, settings):
        popup = Tk()
        popup.wm_title("Oxygen")
        popup.geometry('800x480')
        popup.attributes('-fullscreen', True)
        popup.configure(bg= '#161E2E')
        label1 = ttk.Label(popup, text="Select New Oxygen percentage value", font=("Helvetica", 20))
        label1.pack(side="top", fill="x", pady=10)

        text = StringVar(popup)
        text.set("Oxygen [%]"+'\n'+str(settings.oxygen))
        text_btn = Button(popup, textvariable=text,background='#263655',foreground='white',command=lambda: self.send_settings(popup))
        text_btn.config(height=15, width=30, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"oxygen", settings.oxygen+5, text))
        btn2.config(height=15, width=30, state="normal")
        btn2.pack(side="left",fill="x")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"oxygen", settings.oxygen-5, text))
        btn3.config(height=15, width=30, state="normal")
        btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def GraphPlotFlow(self):

        # Parameters
        x_len = 400         # Number of points to display
        y_range = [0, 80]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#263655')
        ax = self.fig.add_subplot(1, 1, 1, facecolor='#263655')
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(0, x_len))
        ys = [random.random()*40 for x in range(x_len)]

        ax.set_ylim(y_range)

        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys)

        # Add labels
        plt.title('Flow over Time')
        plt.xlabel('Samples')
        plt.ylabel('Flow')

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            # Add y to list
            ys.append(self.latest_sensor_data.flow)
            # Limit y list to set number of items
            ys = ys[-x_len:]
            # Update line with new Y values
            line.set_ydata(ys)

            return line,
        # Set up plot to call animate() function periodically

        canvas = FigureCanvasTkAgg(self.fig, master=self.f9)
        canvas.get_tk_widget().place(x=0, y=0, relwidth=1,relheight=1)
        self.flow_animation_ref = animation.FuncAnimation(self.fig,
           animate,
           fargs=(ys,),
           interval=100,
           blit=True)

    def GraphPlotPressure(self):

        # Parameters
        x_len = 400         # Number of points to display
        y_range = [0, 80]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#263655')
        ax = self.fig.add_subplot(1, 1, 1, facecolor='#263655')
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(0, x_len))
        ys = [random.random()*40 for x in range(x_len)]

        ax.set_ylim(y_range)

        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys)

        # Add labels
        plt.title('Pressure over Time')
        plt.xlabel('Samples')
        plt.ylabel('Pressure (mmHg)')

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            # Add y to list
            ys.append(self.latest_sensor_data.pressure_1_pa)

            # Limit y list to set number of items
            ys = ys[-x_len:]
            # Update line with new Y values
            line.set_ydata(ys)

            return line,
        # Set up plot to call animate() function periodically

        canvas = FigureCanvasTkAgg(self.fig, master=self.f13)
        canvas.get_tk_widget().place(x=0, y=0, relwidth=1,relheight=1)
        self.pressure_animation_ref = animation.FuncAnimation(self.fig,
            animate,
            fargs=(ys,),
            interval=50,
            blit=True)


    def checkAllAlarms(self, settings: Settings, sensors: Sensors):
        if sensors.pressure_1_pa > settings.max_pressure:
            self.pres_btn.configure(background="#FF0749")
            self.giveAlarm()
        else:
            self.pres_btn.configure(background="#263655")

        if sensors.pressure_2_pa < settings.min_pressure: #peep
            self.peep_btn.configure(background="#FF0749")
            self.giveAlarm()
        else:
            self.peep_btn.configure(background="#263655")

            #if valueTida > MaxTV:
            #   lbl7.configure(foreground="red")
            #    giveAlarm()
            #else:
            #    lbl7.configure(foreground="black")

            #if valueTida < MinTV:
            #    lbl8.configure(foreground="red")
            #    giveAlarm()
            #else:
            #    lbl8.configure(foreground="black")

        if sensors.oxygen > settings.max_fio2:
            self.oxy_btn.configure(background="#FF0749")
            self.giveAlarm()
        elif sensors.oxygen < settings.min_fio2:
            self.oxy_btn.configure(background="#FF0749")
            self.giveAlarm()
        else:
            self.oxy_btn.configure(background="#263655")

    def BuildGui(self):
        self.configure(bg= '#161E2E')
        style = ttk.Style()
        style.configure("style.TButton",background='#263655')
        ttk.Style().configure("TButton", padding=6, relief="flat",background='#263655',foreground='#FFFFFF')
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=13, family="Helvetica Neue")


        #define grid sizes and frames
        f1 = ttk.Frame(self, width=160, height=60, borderwidth=1)
        f2 = ttk.Frame(self, width=60, height=60, borderwidth=1)
        f3 = ttk.Frame(self, width=340, height=60, borderwidth=1)
        f4 = ttk.Frame(self, width=120, height=60, borderwidth=1)
        f5 = ttk.Frame(self, width=120, height=60, borderwidth=1)
        f6 = ttk.Frame(self, width=160, height=84, borderwidth=1)
        f7 = ttk.Frame(self, width=160, height=84, borderwidth=1)
        f8 = ttk.Frame(self, width=580, height=504, borderwidth=1) #dual frame
        self.f9 = ttk.Frame(f8, width=576, height=208, borderwidth=0)
        f10 = ttk.Frame(self, width=220, height=84, borderwidth=1)
        f11 = ttk.Frame(self, width=220, height=84, borderwidth=1)
        f12 = ttk.Frame(self, width=220, height=84, borderwidth=1)
        self.f13 = ttk.Frame(f8, width=576, height=208, borderwidth=0)

        f1.grid(row=0, column=0)
        f2.grid(row=0, column=1)
        f3.grid(row=0, column=2)
        f4.grid(row=0, column=3)
        f5.grid(row=0, column=5)
        f6.grid(row=1, column=0)
        f7.grid(row=2, column=0)
        f8.grid(row=1, column=2,rowspan=6,columnspan=4)
        #self.f9.grid(row=1, column=2, columnspan=4, rowspan=3)
        self.f9.grid(row=0, column=0)
        f10.grid(row=3, column=0, columnspan=2)
        f11.grid(row=4, column=0, columnspan=2)
        f12.grid(row=5, column=0, columnspan=2)
        self.f13.grid(row=1,column=0)
        #self.f13.grid(row=4, column=2, columnspan=4, rowspan=3)


        air_btn_text = StringVar()
        air_btn_text.set("OperationAir")
        air_btn = Button(f1, textvariable=air_btn_text,background='#263655',foreground='white')
        air_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.alarm_btn_text = StringVar()
        self.alarm_btn_text.set("Alarm")
        self.alarm_btn = Button(f2, textvariable=self.alarm_btn_text,background='#263655',foreground='white',command = lambda: AlarmPop(self,self.settings))
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
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep)+" [mmHg]")
        self.peep_btn = Button(f6, textvariable=self.peep_btn_text,background='#263655',foreground='white',command = lambda: self.PeepPop(self.settings))
        self.peep_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.tv_btn_text = StringVar()
        self.tv_btn_text.set("Tidal Volume"+'\n'+str()+" [L/min]")
        self.tv_btn = Button(f10, textvariable=self.tv_btn_text,background='#263655',foreground='white')
        self.tv_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.pres_btn_text = StringVar()
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure)+" [mmHg]")
        self.pres_btn = Button(f11, textvariable=self.pres_btn_text,background='#263655',foreground='white',command = lambda: self.PresPop(self.settings) )
        self.pres_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.oxy_btn_text = StringVar()
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen)+" [%]")
        self.oxy_btn = Button(f12, textvariable=self.oxy_btn_text,background='#263655',foreground='white', command = lambda: self.O2Pop(self.settings) )
        self.oxy_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.GraphPlotFlow()
        self.GraphPlotPressure()

    def quit(self, _signal=None, _=None):
        print('ventilator.quit()')
        self._thread_alive = False
        self.mcu.disconnect()
        plt.close('all')
        if self.io_thread:
            self.io_thread.join()
            print('io thread joined')
        if self.pressure_animation_ref:
            self.pressure_animation_ref.running = False
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

            self.mcu.request_sensor_data()

            if not self.sensor_queue.empty():
                sensors = self.sensor_queue.get()
                self.latest_sensor_data = sensors
                print('new sensor data:', sensors)


            if not self.settings_queue.empty():
                settings = self.settings_queue.get()
                    # TODOcheck settings
                    # if mismatch, send settings again
                print("Got settings back: ", settings)

            self.checkAllAlarms(self.settings, self.latest_sensor_data)
            time.sleep(0.04)
        print ('exit app thread')



if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.title("Operation Air Ventilator")
    app.geometry('800x480')
    signal.signal(signal.SIGINT, app.quit)
    app.attributes('-fullscreen', FULLSCREEN)
    gut.center(app)
    app.mainloop()

    print ('bye')
