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

        self.settings = Settings.fromConfig()

        config = ConfigValues()
        self.viewController = ViewController()


    def showMainView(self):
        self.viewController.mainloop()

if __name__ == "__main__":
    app = App()
    app.viewController.asyncio()

    app.showMainView()

    print ('bye')
