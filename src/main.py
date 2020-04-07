import matplotlib
import tkinter as tk

from controllers.communicationController import Microcontroller

matplotlib.use("TkAgg")

from controllers.viewController import ViewController
from models.mcuSettingsModel import Settings

from utils import logger
from utils.config import ConfigValues
from queue import Queue

LOGGING_ENABLED = True
LOGDIR = '../logs'

class App():
    def __init__(self):

        self.settings = Settings.fomConfig()

        config = ConfigValues()
        self.SIMULATE = config.values["developer"]["simulate"]
        self.TTY = config.values['developer']['commPort']
        self.BAUDRATE = config.values['developer']['baudrate']

        self.sensor_queue = Queue()
        self.settings_queue = Queue()
        self.mcu = Microcontroller(self.TTY, self.BAUDRATE, self.settings_queue, self.sensor_queue, simulate=self.SIMULATE)

        self.viewController = ViewController(self.settings, self.mcu)

        self._thread_alive = True
        self.io_thread = None

    def showMainView(self):
        self.viewController.mainloop()

    def asyncio(self):

        if self.settings.start:
            self.req_sensors()
            if self.latest_sensor_data.cycle_state:
                self.checkAllAlarms(self.settings, self.latest_sensor_data)
            self.update_buttons()

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

        if self._thread_alive:
            self.after(100,self.asyncio)

if __name__ == "__main__":
    app = App()
    app.asyncio()
 #   app.mainloop()

    app.showMainView()

    print ('bye')
