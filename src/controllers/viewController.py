import signal
import tkinter as tk
from utils.config import ConfigValues
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import tkinter as tk

from threading import Thread

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from queue import Queue
from tkinter import ttk, BOTH, N, S, E, W
from tkinter import StringVar, Button, Tk, Label
from models.mcuSettingsModel import Settings
from models.mcuSensorModel import Sensors
from controllers.alarmController import registerAlarm
from controllers.communicationController import Microcontroller
from controllers.alarmController import AlarmController, AlarmType

from views.mainView import MainView, MainViewActions
from views.changeSingleSettingView import ChangeSingleSettingView
from views.alarmSettingsOverview import AlarmSettingsOverview
from views.alarmOverview import AlarmOverview
from views.changeDoubleSettingView import ChangeDoubleSettingView, ChangeAlarmViewActions
from views.activeAlarmView import alarm_overview
from views.menuView import MenuView, MenuViewActions

from utils.constants import SettingType


from utils import logger

class ViewController(tk.Tk):

    def __init__(self):
        super().__init__()

        self.settings = Settings.fromConfig()

        self.config = ConfigValues()

        self._thread_alive = True
        self.io_thread = None

        self.SIMULATE = self.config.values["developer"]["simulate"]
        self.TTY = self.config.values['developer']['commPort']
        self.BAUDRATE = self.config.values['developer']['baudrate']
        self.LOGGING_ENABLED = self.config.values['developer']['logEnabled']
        self.LOGDIR = self.config.values['developer']['logDir']

        self.tv_step = self.config.values['defaultSettings']['tv_step']
        self.fio2_step = self.config.values['defaultSettings']['fio2_step']
        self.peep_step = self.config.values['defaultSettings']['peep_step']
        self.press_step = self.config.values['defaultSettings']['pressure_step']
        self.ratio_step = self.config.values['defaultSettings']['ratio_step']
        self.freq_step = self.config.values['defaultSettings']['freq_step']

        self.sensor_queue = Queue()
        self.settings_queue = Queue()
        self.mcu = Microcontroller(self.TTY, self.BAUDRATE, self.settings_queue, self.sensor_queue, simulate=self.SIMULATE)
        self.alarms = AlarmController()
        # for RPi

        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title("Operation Air Ventilator")
        self.geometry('800x480')
        signal.signal(signal.SIGINT, self.quit)
        self.attributes('-fullscreen', self.config.values['window']['fullscreen'])
        self.center()

        # For plotting
        self.line_pressure = None
        self.line_flow = None
        self.ys_p = []
        self.ys_f = []
        self.pressure_animation_ref = None

        self.log_handle = None

        self.latest_sensor_data = Sensors.default()

        self.setStyle()

        self.menuView = None
        self.mainView = MainView(self.winfo_width(), self.winfo_height(), self.settings, self.latest_sensor_data, self.mainViewCallback)

        self.mainView.pack(fill=BOTH, expand=True)
        self.io_thread = Thread(target=self.asyncio)
        self.io_thread.daemon = True
        self.io_thread.start()
        print(self.req_sensors())

    def updateSettings(self, settings):
        self.settings = settings

    def alarmSettingsOverviewCallback(self, type):
        if type == SettingType.PEEP:
            min_peep = self.config.values['alarmSettings']['min_peep']
            max_peep = self.config.values['alarmSettings']['max_peep']
            self.settingsView = ChangeDoubleSettingView(SettingType.PEEP, self.settings.min_peep, min_peep, max_peep, self.peep_step,
                                                        self.settings.max_peep, min_peep, max_peep, self.peep_step, "PEEP [cm H2O]",
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif type == SettingType.OXYGEN:
            min_fio2 = self.config.values['alarmSettings']['min_fio2']
            max_fio2 = self.config.values['alarmSettings']['max_fio2']
            self.settingsView = ChangeDoubleSettingView(SettingType.OXYGEN, self.settings.min_fio2, min_fio2, max_fio2, self.fio2_step,
                                                        self.settings.max_fio2, min_fio2, max_fio2, self.fio2_step, "Oxygen [O2]",
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif type == SettingType.TIDAL:
            min_tv = self.config.values['alarmSettings']['min_tv']
            max_tv = self.config.values['alarmSettings']['max_tv']
            self.settingsView = ChangeDoubleSettingView(SettingType.TIDAL, self.settings.min_tv, min_tv, max_tv, self.tv_step,
                                                        self.settings.max_tv, min_tv, max_tv, self.tv_step, "Tidal Volume",
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif type == SettingType.PRESSURE:
            min_press = self.config.values['alarmSettings']['min_pressure']
            max_press = self.config.values['alarmSettings']['max_pressure']
            self.settingsView = ChangeDoubleSettingView(SettingType.PRESSURE, self.settings.min_pressure, min_press, max_press, self.press_step,
                                                        self.settings.max_pressure, min_press, max_press, self.press_step, "Pressure [cm H2O]",
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()

        self.alarmSettingsOverview.place_forget()

    def changeDoubleValueViewCallback(self, type, val1, val2):
        if type == SettingType.PEEP:
            self.settings.min_peep = val1
            self.settings.max_peep = val2
        elif type == SettingType.OXYGEN:
            self.settings.min_fio2 = val1
            self.settings.max_fio2 = val2
        elif type == SettingType.PRESSURE:
            self.settings.min_pressure = val1
            self.settings.max_pressure = val2
        elif type == SettingType.TIDAL:
            self.settings.min_tv = val1
            self.settings.max_tv = val2
        elif type == SettingType.FREQ:
            self.settings.freq = val1
            self.settings.ratio = int(val2 * 10)
            self.settingsView.place_forget()
            self.mcu.send_settings(self.settings)
            return

        self.settingsView.place_forget()

    def changeSingleSettingCallback(self, type, value):
        if type == SettingType.PEEP:
            self.settings.peep = value
        if type == SettingType.OXYGEN:
            self.settings.oxygen = value
        if type == SettingType.PRESSURE:
            self.settings.pressure = value
        if type == SettingType.PEEP:
            self.settings.peep = value

        self.changeSettingView.place_forget()
        self.mainView.update(self.settings, self.latest_sensor_data)
        self.mcu.send_settings(self.settings)

    def alarmOverviewCallback(self, alarm):
        if alarm == AlarmType.NONE:
            self.alarmOverview.place_forget()
            return
        elif alarm == AlarmType.CLEAR:
            self.alarms.removeInactive()
        else:
            self.alarms.mute(alarm)

        self.alarmOverview.fill_frame()

    def menuViewCallback(self, action):
        print('menuViewCallback')
        if action == MenuViewActions.NONE:
            self.menuView.place_forget()
            return
        elif action == MenuViewActions.SHUTDOWN:
            print("Shutdown Machine")
            self.quit()
            # todo actually shot down os...
        elif action == MenuViewActions.SELF_TEST:
            print("Clicked SELF_TEST: Not implemented")
        elif action == MenuViewActions.INSPIRATORY_HOLD_START:
            print("Clicked INSPIRATORY_HOLD_START")
            self.mcu.try_start_inspiratroy_hold()
        elif action == MenuViewActions.INSPIRATORY_HOLD_STOP:
            print("Clicked INSPIRATORY_HOLD_STOP")
            self.mcu.stop_inspiratroy_hold()
        elif action == MenuViewActions.EXPIRATORY_HOLD_START:
            print("Clicked EXPIRATORY_HOLD_START")
            self.mcu.try_start_expiratroy_hold()
        elif action == MenuViewActions.EXPIRATORY_HOLD_STOP:
            print("Clicked EXPIRATORY_HOLD_STOP")
            self.mcu.stop_expiratroy_hold()
        else:
            print("Unknown menu action")


    def mainViewCallback(self, action):
        if action == MainViewActions.QUIT:
            print("Clicked Quitting")
            self.quit()
        elif action == MainViewActions.MENU:
            print("Clicked MENU")
            self.menuView = MenuView(callback=self.menuViewCallback)
            self.menuView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.menuView.fill_frame()

        elif action == MainViewActions.ALARM:
            self.alarmSettingsOverview = AlarmSettingsOverview(self.settings, self.alarmSettingsOverviewCallback)
            self.alarmSettingsOverview.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.alarmSettingsOverview.fill_frame()
            print("Clicked Alarm")
        elif action == MainViewActions.VIEW_ALARMS:
            print("Clicked Alarm Overview")
            self.alarmOverview = AlarmOverview(self.alarmOverviewCallback)
            self.alarmOverview.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.alarmOverview.fill_frame()

        elif action == MainViewActions.PATIENT:
            print("Clicked Patient")
            self.mcu.try_start_inspiratroy_hold()
        elif action == MainViewActions.STARTSTOP:
            print("Clicked Startstop")
            self.start()
        elif action == MainViewActions.PEEP:
            print("Clicked PEEP")
            min_peep = self.config.values['defaultSettings']['min_peep']
            max_peep = self.config.values['defaultSettings']['max_peep']
            self.changeSettingView = ChangeSingleSettingView(SettingType.PEEP, self.settings.peep, min_peep,
                                                             max_peep, self.peep_step, "PEEP \n[cm H2O]", self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        elif action == MainViewActions.FREQ:
            print("Clicked Freq")
            min_freq = self.config.values['defaultSettings']['min_freq']
            max_freq = self.config.values['defaultSettings']['max_freq']
            self.settingsView = ChangeDoubleSettingView(SettingType.FREQ, self.settings.freq, min_freq, max_freq, self.freq_step,
                                                        self.settings.ratio / 10, 1, 3, self.ratio_step, "Frequency and Ratio",
                                                        self.changeDoubleValueViewCallback, "Freq \n[1/min]", "Ratio (1:?)", bound=False)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
            #self.changeSettingView = ChangeSingleSettingView(SettingType.FREQ, self.settings.freq,
                                                           #  min_freq,
                                                            # max_freq, 1, "Frequency \n[1/min]",
                                                             #self.changeSingleSettingCallback)
            #self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            #self.changeSettingView.fill_frame()
        elif action == MainViewActions.PRESSURE:
            print("Clicked Pressure")
            min_press = self.config.values['defaultSettings']['min_pressure']
            max_press = self.config.values['defaultSettings']['max_pressure']
            self.changeSettingView = ChangeSingleSettingView(SettingType.PRESSURE, self.settings.pressure,
                                                             min_press,
                                                             max_press, self.press_step, "Pressure \n[cm H2O]",
                                                             self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        elif action == MainViewActions.OXYGEN:
            print("Clicked Oxygen")
            min_fio2 = self.config.values['defaultSettings']['min_fio2']
            max_fio2 = self.config.values['defaultSettings']['max_fio2']
            self.changeSettingView = ChangeSingleSettingView(SettingType.OXYGEN, self.settings.oxygen,
                                                             min_fio2,
                                                             max_fio2, self.fio2_step, "Oxygen \n[O2]",
                                                             self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        else:
            print("Unknown action")


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

    def checkAllAlarms(self, settings, sensors):
        self.alarms.checkForNewAlarms(settings, sensors)

    def setStyle(self):
        self.configure(bg= '#161E2E')
        style = ttk.Style()
        style.configure("style.TButton",background='#263655')
        ttk.Style().configure("TButton", padding=6, relief="flat",background='#263655',foreground='#FFFFFF')
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=13, family="Helvetica Neue")


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
            if self.log_handle:
                logger.close_session(self.log_handle)
                self.log_handle = None
        else:
            # send start
            self.settings.start = 1
            if self.LOGGING_ENABLED:
                self.log_handle = logger.start_new_session(directory=self.LOGDIR, file_prefix='sensors', use_csv=True)
        self.mainView.update(self.settings, self.latest_sensor_data)
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
        print("Send settings:", self.settings)


    def asyncio(self):
        if self.settings.start:
            self.req_sensors()
            if self.latest_sensor_data.cycle_state:
                self.checkAllAlarms(self.settings, self.latest_sensor_data)

        if not self.sensor_queue.empty():
            sensors = self.sensor_queue.get()
            self.latest_sensor_data = sensors

            if self.log_handle:
                logger.write_csv(self.log_handle, self.latest_sensor_data.as_list())

        if not self.settings_queue.empty():
            settings = self.settings_queue.get()
            if not self.settings.equals(settings):
                print("MISMATCH SETTINGS: RESEND")
                self.send_settings()

        self.mainView.update(self.settings, self.latest_sensor_data)
        if self.menuView:
            self.menuView.update(self.latest_sensor_data.inspiratory_hold_result,
                                self.latest_sensor_data.expiratory_hold_result)

        if self._thread_alive:
           self.after(100,self.asyncio)