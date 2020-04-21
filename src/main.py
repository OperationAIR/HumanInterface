#!/usr/bin/env python3
from controllers.viewController import ViewController
from models.mcuSettingsModel import Settings
from utils.config import ConfigValues


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
