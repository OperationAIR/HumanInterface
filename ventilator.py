import tkinter as tk
import signal

from settings import Settings
from mcu import Microcontroller

BAUDRATE = 115200
TTY = '/dev/cu.usbmodemC1DDCDF83'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.onbtn = tk.Button(self, text="Led on",
                             command=self.say_hello)
        self.onbtn.pack(padx=120, pady=30)

        self.offbtn = tk.Button(self, text="Led off",
                             command=self.say_bye)
        self.offbtn.pack(padx=220, pady=30)

        self.settingsbtn = tk.Button(self, text="New Settings",
                             command=self.send_settings)
        self.settingsbtn.pack(padx=320, pady=30)

        self.mcu = Microcontroller(TTY, BAUDRATE)

    def say_hello(self):
        print("Hello, Tkinter!")
        self.mcu.led_on()

    def say_bye(self):
        print("Bye, Tkinter!")
        self.mcu.led_off()

    def send_settings(self):
        settings = Settings(
            peep=20,
            freq=20,
            tidal_vol=120,
            pressure=20,
            max_pressure=45,
            min_pressure=5,
            max_tv=400,
            min_tv=200,
            max_fio2=50,
            min_fio2=20)
        self.mcu.send_settings(settings)
        print("Send settings")

    def quit(self, _signal=None, _=None):
        self.mcu.disconnect()
        print('bye')
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.title("Operation Air Ventilator")
    app.geometry('800x480')
    signal.signal(signal.SIGINT, app.quit)
    app.mainloop()





# import tkinter as tk
# from types import SimpleNamespace
# from queue import Queue
# from enum import Enum
# from threading import Thread

# class Messages(Enum):
#     CLICK = 0

# def updatecycle(guiref, model, queue):
#     while True:
#         msg = queue.get()
#         if msg == Messages.CLICK:
#             model.count += 1
#             guiref.label.set("Clicked: {}".format(model.count))

# def gui(root, queue):
#     label = tk.StringVar()
#     label.set("Clicked: 0")
#     tk.Label(root, textvariable=label).pack()
#     tk.Button(root, text="Click me!", command=lambda : queue.put(Messages.CLICK)).pack()
#     return SimpleNamespace(label=label)

# if __name__ == '__main__':
#     root = tk.Tk()
#     queue = Queue()
#     guiref = gui(root, queue)
#     model = SimpleNamespace(count=0)
#     t = Thread(target=updatecycle, args=(guiref, model, queue,))
#     t.daemon = True
#     t.start()
#     tk.mainloop()