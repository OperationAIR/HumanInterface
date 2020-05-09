import subprocess
from queue import Queue
from signal import SIGINT, signal
from threading import Thread
from time import time
from tkinter import BOTH, Tk, font, ttk

import matplotlib.pyplot as plt

from controllers.alarmController import AlarmController, AlarmType
from controllers.communicationController import Microcontroller
from models.mcuSensorModel import Sensors
from models.mcuSettingsModel import Settings
from utils import logger
from utils.airTime import AirTime
from utils.config import ConfigValues
from utils.constants import SettingType
from utils.internationalization import Internationalization
from views.alarmOverview import AlarmOverview
from views.alarmSettingsOverview import AlarmSettingsOverview
from views.changeDoubleSettingView import ChangeDoubleSettingView
from views.changeSingleSettingView import ChangeSingleSettingView
from views.mainView import MainView, MainViewActions
from views.menuView import MenuView, MenuViewActions
from views.setTimeView import SetTimeCallback, SetTimeView


class ViewController(Tk):

    def __init__(self):
        super().__init__()

        # We start by requesting current settings from mcu
        # in case the mcu was alread
        self.settings = Settings.fromConfig()
        self.settings_initialized = False

        self.config = ConfigValues()

        Internationalization()

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
        self.title(_("Operation Air Ventilator"))
        self.geometry('800x480')
        signal(SIGINT, self.quit)
        self.attributes('-fullscreen', self.config.values['window']['fullscreen'])
        self.center()

        self.log_handle = None

        self.latest_sensor_data = Sensors.default()

        self.setStyle()

        self.menuView = None

        self.setTimeView = SetTimeView(self.setTimeCallback)
        self.mainView = MainView(self.winfo_width(), self.winfo_height(), self.settings, self.latest_sensor_data, self.mainViewCallback)

        self.setTimeView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())

        self.request_sensor_timestamp = None
        self.request_timeout = 10

        self.io_thread = Thread(target=self.asyncio)
        self.io_thread.daemon = True
        self.io_thread.start()
        # self.mcu.request_settings()
        self.mcu.request_sensor_data()

    def setTimeCallback(self, sttype, time):

        airtime = AirTime()

        if sttype == SetTimeCallback.SET_TIME:
            airtime.setTime(time)
            print("Set time to " + airtime.time)
        self.setTimeView.place_forget()
        self.mainView.pack(fill=BOTH, expand=True)

    def updateSettings(self, settings):
        self.settings = settings

    def alarmSettingsOverviewCallback(self, stype):
        if stype == SettingType.PEEP:
            min_peep = self.config.values['alarmSettings']['min_peep']
            max_peep = self.config.values['alarmSettings']['max_peep']
            self.settingsView = ChangeDoubleSettingView(SettingType.PEEP, self.settings.min_peep, min_peep, max_peep, self.peep_step,
                                                        self.settings.max_peep, min_peep, max_peep, self.peep_step, _("PEEP") + " " + _("[cm H2O]"),
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif stype == SettingType.OXYGEN:
            min_fio2 = self.config.values['alarmSettings']['min_fio2']
            max_fio2 = self.config.values['alarmSettings']['max_fio2']
            self.settingsView = ChangeDoubleSettingView(SettingType.OXYGEN, self.settings.min_fio2, min_fio2, max_fio2, self.fio2_step,
                                                        self.settings.max_fio2, min_fio2, max_fio2, self.fio2_step, _("Oxygen") + " " + _("[O2]"),
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif stype == SettingType.TIDAL:
            min_tv = self.config.values['alarmSettings']['min_tv']
            max_tv = self.config.values['alarmSettings']['max_tv']
            self.settingsView = ChangeDoubleSettingView(SettingType.TIDAL, self.settings.min_tv, min_tv, max_tv, self.tv_step,
                                                        self.settings.max_tv, min_tv, max_tv, self.tv_step, _("Tidal Volume"),
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()
        elif stype == SettingType.PRESSURE:
            min_press = self.config.values['alarmSettings']['min_pressure']
            max_press = self.config.values['alarmSettings']['max_pressure']
            self.settingsView = ChangeDoubleSettingView(SettingType.PRESSURE, self.settings.min_pressure, min_press, max_press, self.press_step,
                                                        self.settings.max_pressure, min_press, max_press, self.press_step, _("Pressure") + " " + _("[cm H2O]"),
                                                        self.changeDoubleValueViewCallback)
            self.settingsView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.settingsView.fill_frame()

        self.alarmSettingsOverview.place_forget()

    def changeDoubleValueViewCallback(self, stype, val1, val2):
        if stype == SettingType.PEEP:
            self.settings.min_peep = val1
            self.settings.max_peep = val2
        elif stype == SettingType.OXYGEN:
            self.settings.min_fio2 = val1
            self.settings.max_fio2 = val2
        elif stype == SettingType.PRESSURE:
            self.settings.min_pressure = val1
            self.settings.max_pressure = val2
        elif stype == SettingType.TIDAL:
            self.settings.min_tv = val1
            self.settings.max_tv = val2
        elif stype == SettingType.FREQ:
            self.settings.freq = val1
            self.settings.ratio = int(val2 * 10)
            self.settingsView.place_forget()
            self.mcu.send_settings(self.settings)
            return

        self.settingsView.place_forget()

    def changeSingleSettingCallback(self, stype, value):
        if stype == SettingType.PEEP:
            self.settings.peep = value
        if stype == SettingType.OXYGEN:
            self.settings.oxygen = value
        if stype == SettingType.PRESSURE:
            self.settings.pressure = value
        if stype == SettingType.PEEP:
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
            print("Shutting down Machine")
            hard_shutdown = self.config.values['developer']['hardShutdown']
            if not hard_shutdown:
                self.quit()
            else:
                try:
                    subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
                except ValueError:
                    print("Failed to shutdown")

            return
        elif action == MenuViewActions.SELF_TEST:
            print("Clicked SELF_TEST: Not implemented")
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
            self.menuView.fill_frame(self.settings)

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
        elif action == MainViewActions.STARTSTOP:
            print("Clicked Startstop")
            self.start()
        elif action == MainViewActions.PEEP:
            print("Clicked PEEP")
            min_peep = self.config.values['defaultSettings']['min_peep']
            max_peep = self.config.values['defaultSettings']['max_peep']
            self.changeSettingView = ChangeSingleSettingView(SettingType.PEEP, self.settings.peep, min_peep,
                                                             max_peep, self.peep_step, _("PEEP") + "\n" + _("[cm H2O]"), self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        elif action == MainViewActions.FREQ:
            print("Clicked Freq")
            min_freq = self.config.values['defaultSettings']['min_freq']
            max_freq = self.config.values['defaultSettings']['max_freq']
            min_ratio = 0.5 # TODO should go in config
            max_ratio = 3 # TODO should go in config
            self.settingsView = ChangeDoubleSettingView(SettingType.FREQ, self.settings.freq, min_freq, max_freq, self.freq_step,
                                                        self.settings.ratio / 10, min_ratio, max_ratio, self.ratio_step, _("Frequency and Ratio"),
                                                        self.changeDoubleValueViewCallback, _("Freq") + "\n" + _("[1/min]"), _("Ratio") + " (1:?)", bound=False)
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
                                                             max_press, self.press_step, _("PC above PEEP") + "\n" + _("[cm H2O]"),
                                                             self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        elif action == MainViewActions.OXYGEN:
            print("Clicked Oxygen")
            min_fio2 = self.config.values['defaultSettings']['min_fio2']
            max_fio2 = self.config.values['defaultSettings']['max_fio2']
            self.changeSettingView = ChangeSingleSettingView(SettingType.OXYGEN, self.settings.oxygen,
                                                             min_fio2,
                                                             max_fio2, self.fio2_step, _("Oxygen") + "\n" + _("[O2]"),
                                                             self.changeSingleSettingCallback)
            self.changeSettingView.place(x=0, y=0, width=self.winfo_width(), height=self.winfo_height())
            self.changeSettingView.fill_frame()
        elif action == MainViewActions.INSP_HOLD_START:
            print("Insp Hold Start")
            self.mcu.try_start_inspiratory_hold()
        elif action == MainViewActions.INSP_HOLD_STOP:
            print("Insp Hold Stop")
            self.mcu.stop_inspiratory_hold()
        elif action == MainViewActions.EXP_HOLD_START:
            print("Exp hold start")
            self.mcu.try_start_expiratory_hold()
        elif action == MainViewActions.EXP_HOLD_STOP:
            print("Exp hold stop")
            self.mcu.stop_expiratory_hold()
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
            textR.set(_("Ratio")+'\n'+'1:3')
        elif settings.ratio == 3:
            settings.ratio = 1
            textR.set(_("Ratio")+'\n'+'1:1')
        else:
            settings.ratio = 2
            textR.set(_("Ratio")+'\n'+'1:2')

    def checkAllAlarms(self, settings, sensors):
        self.alarms.checkForNewAlarms(settings, sensors)

    def setStyle(self):
        self.configure(bg= '#161E2E')
        style = ttk.Style()
        style.configure("style.TButton",background='#263655')
        ttk.Style().configure("TButton", padding=6, relief="flat",background='#263655',foreground='#FFFFFF')
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=13, family="Helvetica Neue")

    def destroy_async(self): self.destroy()

    def quit(self, _signal=None, _=None):
        self._thread_alive = False
        self.mcu.disconnect()
        plt.close('all')
        if self.io_thread: self.io_thread.join()
        self.after(300, self.destroy_async)

    def start(self):
        self.alarms.resetStartDelay()
        self.request_sensor_timestamp = None
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

    def send_settings(self, popup=None):
        self.mcu.send_settings(self.settings)
        print("Send settings:", self.settings)


    def asyncio(self):
        if self.settings.start:
            self.mcu.request_sensor_data()

            can_start = self.alarms.checkStartDelay(self.settings)

            if can_start and self.request_sensor_timestamp is None:
                self.request_sensor_timestamp = time()

            if self.latest_sensor_data.cycle_state:
                self.checkAllAlarms(self.settings, self.latest_sensor_data)

        if not self.sensor_queue.empty():
            sensors = self.sensor_queue.get()
            self.latest_sensor_data = sensors

            if self.log_handle:
                logger.write_csv(self.log_handle, self.latest_sensor_data.as_list())
            
            self.alarms.removeAlarm(AlarmType.MCU_DISCONNECTED)

        elif self.settings.start and self.request_sensor_timestamp != None:
            timeDiff = time() - self.request_sensor_timestamp
            if timeDiff > self.request_timeout:
                self.alarms.addAlarm(AlarmType.MCU_DISCONNECTED)
                self.request_sensor_timestamp = None


        if not self.settings_queue.empty():
            mcuSettings = self.settings_queue.get()
            if not self.settings_initialized:
                self.settings = Settings.from_mcuSettings(mcuSettings)
                # Todo, maybe verify settings
                self.settings_initialized = True
                print('settings initialized')
            elif not self.settings.equals(mcuSettings):
                print("MISMATCH SETTINGS: RESEND")
                self.send_settings()

        if not self.settings_initialized:
            self.mcu.request_settings()

        self.mainView.update(self.settings, self.latest_sensor_data)
        if self.menuView:
            self.menuView.update(self.settings)

        if self._thread_alive:
           self.after(100,self.asyncio)
