import signal
import tkinter as tk
from utils.config import ConfigValues
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import tkinter as tk

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from queue import Queue
from tkinter import ttk
from tkinter import StringVar, Button, Tk
from models.mcuSettingsModel import Settings
from models.mcuSensorModel import Sensors
from controllers.alarmController import playAlarm
from views.activeAlarmView import alarm_overview
from views.alarmSettingsView import AlarmPop
from controllers.communicationController import Microcontroller


from utils import logger

class ViewController(tk.Tk):

    def __init__(self, settings, mcu):
        super().__init__()

        self.settings = settings
        self.mcu = mcu

        config = ConfigValues()

        # for RPi
        self.LOGGING_ENABLED = config.values['developer']['logEnabled']
        self.LOGDIR = config.values['developer']['logDir']

        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title("Operation Air Ventilator")
        self.geometry('800x480')
        signal.signal(signal.SIGINT, self.quit)
        self.attributes('-fullscreen', config.values['window']['fullscreen'])
        self.center()

        # For plotting
        self.line_pressure = None
        self.line_flow = None
        self.ys_p = []
        self.ys_f = []
        self.pressure_animation_ref = None

        self.log_handle = None

        self.latest_sensor_data = Sensors.default()


        self.BuildGui()
        # self.io_thread = Thread(target=self.asyncio)
        # self.io_thread.daemon = True
        # self.io_thread.start()
        print(self.req_sensors())

    def updateSettings(self, settings):
        self.settings = settings

    def center(self):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        self.update_idletasks()
        width = self.winfo_width()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = width + 2 * frm_width
        height = self.winfo_height()
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()

    def giveAlarm(self):
        pass # print("alarm!!")

    def setValues(self, settings, popup, valuetype, value, text):
        if valuetype == "peep":
            if value <= 35 and value >= 5:
                settings.peep = value
            text.set("Confirm \n PEEP"+'\n'+str(settings.peep))
            return
        if valuetype == "freq":
            if value <= 30 and value >= 5:
                settings.freq = value
            text.set("Confirm \n Frequency"+'\n'+str(settings.freq))
            return
        if valuetype == "pres":
            if value <= 70 and value >= 10:
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
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep)+" [cm H2O]")
        self.tv_btn_text.set("Tidal Volume\n"+str(self.latest_sensor_data.minute_volume)+" [L/min]\n"+str(self.latest_sensor_data.tidal_volume)+" [mL]")
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure)+" [cm H2O]")
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen)+" [%]"+'\n'+"Current: "+str(self.latest_sensor_data.oxygen)+" [%]")

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
        text_btn.config(height=15, width=20, state="normal")
        text_btn.pack(side="left")

        btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq+1, text))
        btn2.config(height=15, width=20, state="normal")
        btn2.pack(side="left")

        btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: self.setValues(settings, popup,"freq", settings.freq-1, text))
        btn3.config(height=15, width=20, state="normal")
        btn3.pack(side="left")

        textR = StringVar(popup)
        textR.set("Ratio"+'\n'+'1:2')
        btn4 = Button(popup, textvariable=textR,background='#263655',foreground='white', command=lambda: self.setRatio(settings, textR))
        btn4.config(height=15, width=30, state="normal")
        btn4.pack(side="left")

        popup.mainloop()
        return

    def setRatio(self, settings, textR):
        if settings.ratio == 2:
            settings.ratio = 3
            textR.set("Ratio"+'\n'+'1:3')
        elif settings.ratio == 3:
            settings.ratio = 1
            textR.set("Ratio"+'\n'+'1:1')
        else:
            settings.ratio = 2
            textR.set("Ratio"+'\n'+'1:2')

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
        y_range = [-30, 0]  # Range of possible Y values to display

        # Create figure for plotting
        self.fig = plt.figure()
        self.fig.patch.set_facecolor('#263655')
        ax = self.fig.add_subplot(1, 1, 1, facecolor='#263655')
        #ax.spines['bottom'].set_color('gray')

        xs = list(range(0, x_len))
        ys = [0 for x in range(x_len)]

        ax.set_ylim(y_range)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.get_yaxis().tick_left()
        ax.yaxis.label.set_size(13)
        ax.yaxis.label.set_color('white')
        plt.setp(ax.get_xticklabels(), visible=False)

        plt.yticks(fontsize=13, color='white')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")
        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color= '#43DBA7')

        # Add labels
        plt.title('Flow', fontsize= 13, color="white")
        #plt.xlabel('Samples')
        plt.ylabel('[L/min]')


        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            if not self.settings.start:
                return line,
            # Add y to list
            ys.append(-1*self.latest_sensor_data.flow)
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
        ys = [0 for x in range(x_len)]

        ax.set_ylim(y_range)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("white")
        ax.get_yaxis().tick_left()
        ax.yaxis.label.set_size(13)
        ax.yaxis.label.set_color('white')
        plt.setp(ax.get_xticklabels(), visible=False)

        plt.yticks(fontsize=13, color='white')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")
        # Create a blank line. We will update the line in animate
        line, = ax.plot(xs, ys, color= '#EBE1D0')

        # Add labels
        plt.title('Pressure', fontsize= 13, color="white")
        #plt.xlabel('Samples')
        plt.ylabel('[cm H2O]')

        # This function is called periodically from FuncAnimation
        def animate(i, ys):

            if not self.settings.start:
                return line,
            # Add y to list
            ys.append(self.latest_sensor_data.pressure)

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
            interval=100,
            blit=True)


    def checkAllAlarms(self, settings: Settings, sensors: Sensors):
        if (not sensors.peep) and sensors.pressure > settings.max_pressure:
            self.pres_btn.configure(background="#FF0749")
            playAlarm()

        elif (not sensors.peep) and sensors.pressure < settings.min_pressure:
            self.pres_btn.configure(background="#FF0749")
            playAlarm()

        else:
            self.pres_btn.configure(background="#263655")

        if sensors.peep and sensors.peep > settings.min_peep:
            self.pres_btn.configure(background="#FF0749")
            playAlarm()

        else:
            self.peep_btn.configure(background="#263655")

        if sensors.tidal_volume > settings.max_tv:
            self.tv_btn.configure(background="#FF0749")
            playAlarm()

        elif sensors.tidal_volume < settings.min_tv:
            self.tv_btn.configure(background="#FF0749")
            playAlarm()
        else:
            self.tv_btn.configure(background="#263655")

        if sensors.oxygen > settings.max_fio2:
            self.oxy_btn.configure(background="#FF0749")
            playAlarm()
        elif sensors.oxygen < settings.min_fio2:
            self.oxy_btn.configure(background="#FF0749")
            playAlarm()
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
        f1 = tk.Frame(self, width=160, height=60, borderwidth=1, bg='#161E2E')
        f2 = tk.Frame(self, width=60, height=60, borderwidth=1, bg='#161E2E')
        f3 = tk.Frame(self, width=340, height=60, borderwidth=1, bg='#161E2E')
        f4 = tk.Frame(self, width=120, height=60, borderwidth=1, bg='#161E2E')
        f5 = tk.Frame(self, width=120, height=60, borderwidth=1, bg='#161E2E')
        f6 = tk.Frame(self, width=220, height=84, borderwidth=1, bg='#161E2E') #160
        f7 = tk.Frame(self, width=220, height=84, borderwidth=1, bg='#161E2E') #160
        f8 = tk.Frame(self, width=580, height=504, borderwidth=1, bg='#161E2E') #dual frame
        self.f9 = tk.Frame(f8, width=576, height=208, borderwidth=0, bg='#161E2E')
        f10 = tk.Frame(self, width=220, height=84, borderwidth=1, bg='#161E2E')
        f11 = tk.Frame(self, width=220, height=84, borderwidth=1, bg='#161E2E')
        f12 = tk.Frame(self, width=220, height=84, borderwidth=1, bg='#161E2E')
        self.f13 = tk.Frame(f8, width=576, height=208, borderwidth=0, bg='#161E2E')

        f1.grid(row=0, column=0)
        f2.grid(row=0, column=1)
        f3.grid(row=0, column=2)
        f4.grid(row=0, column=3)
        f5.grid(row=0, column=5)
        f6.grid(row=1, column=0, columnspan=2)
        f7.grid(row=2, column=0, columnspan =2)
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
        air_btn = Button(f1, textvariable=air_btn_text,background='#263655',highlightbackground='#161E2E', foreground='white',command = lambda: self.quit())
        air_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.alarm_btn_text = StringVar()
        self.alarm_btn_text.set("Alarm")
        self.alarm_btn = Button(f2, textvariable=self.alarm_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: AlarmPop(self,self.settings))
        self.alarm_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.alarm_name_btn_text = StringVar()
        self.alarm_name_btn_text.set("Alarm overview")
        self.alarm_name_btn = Button(f3, textvariable=self.alarm_name_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: alarm_overview(self,self.settings))
        self.alarm_name_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.patient_btn_text = StringVar()
        self.patient_btn_text.set("Patient")
        self.patient_btn = Button(f4, textvariable=self.patient_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white', comman = lambda:  self.mcu.try_start_inspiratroy_hold() )
        self.patient_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.switch_btn_text = StringVar()
        self.switch_btn_text.set("Start")
        self.switch_btn = Button(f5, textvariable=self.switch_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: self.start())
        self.switch_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.freq_btn_text = StringVar()
        self.freq_btn_text.set("Frequency"+'\n'+str(self.settings.freq)+" [1/min]")
        self.freq_btn = Button(f7, textvariable=self.freq_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: self.FreqPop(self.settings))
        self.freq_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.peep_btn_text = StringVar()
        self.peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep)+" [cm H2O]")
        self.peep_btn = Button(f6, textvariable=self.peep_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: self.PeepPop(self.settings))
        self.peep_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.tv_btn_text = StringVar()
        self.tv_btn_text.set("Tidal Volume"+'\n'+str()+" [mL]")
        self.tv_btn = Button(f10, textvariable=self.tv_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white')
        self.tv_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.pres_btn_text = StringVar()
        self.pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure)+" [cm H2O]")
        self.pres_btn = Button(f11, textvariable=self.pres_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white',command = lambda: self.PresPop(self.settings) )
        self.pres_btn.place(x=0, y=0, relwidth=1,relheight=1)

        self.oxy_btn_text = StringVar()
        self.oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen)+" [%]")
        self.oxy_btn = Button(f12, textvariable=self.oxy_btn_text,background='#263655',highlightbackground='#161E2E',foreground='white', command = lambda: self.O2Pop(self.settings) )
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

    def start(self):

        if self.settings.start == 1:
            # send stop
            self.settings.start = 0
            self.switch_btn_text.set("Start")
            if self.log_handle:
                logger.close_session(self.log_handle)
                self.log_handle = None
        else:
            # send start
            self.settings.start = 1
            self.switch_btn_text.set("Stop")
            if self.LOGGING_ENABLED:
                self.log_handle = logger.start_new_session(directory=self.LOGDIR, file_prefix='sensors', csv=True)
        self.send_settings()

    def say_hello(self):
        print("Hello, Tkinter!")
        self.mcu.led_on()

    def say_bye(self):
        print("Bye, Tkinter!")
        self.mcu.led_off()

    def req_sensors(self):
        self.mcu.request_sensor_data()

    def send_settings(self, popup=None):
        self.mcu.send_settings(self.settings)
        self.update_buttons()
        if popup:
            popup.destroy()
        print("Send settings:", self.settings)