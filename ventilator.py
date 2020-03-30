import tkinter as tk
import signal
import time
from threading import Thread
from queue import Queue
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar, Button, Tk

from settings import Settings
from mcu import Microcontroller

BAUDRATE = 115200
TTY = '/dev/cu.usbserial-A50285BI'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.settings = Settings(
            peep=20,
            freq=20,
            ratio=2,
            tidal_vol=120,
            pressure=20,
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

        # btn2 = Button(popup, text="+",background='#263655',foreground='white', command=lambda: setValues(popup,"freq", valueFreq+5, text))
        # btn2.config(height=5, width=10, state="normal")
        # btn2.pack(side="left",fill="x")

        # btn3 = Button(popup, text="-",background='#263655',foreground='white', command=lambda: setValues(popup,"freq", valueFreq-5, text))
        # btn3.config(height=5, width=10, state="normal")
        # btn3.pack(side="left",fill="x")

        popup.mainloop()
        return

    def BuildGui(self):
        self.configure(bg= '#161E2E')
        style = ttk.Style()
        style.configure("style.TButton",background='#263655')
        ttk.Style().configure("TButton", padding=6, relief="flat",background='#263655',foreground='white')
    
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
        air_btn = ttk.Button(f1, textvariable=air_btn_text)
        air_btn.place(x=0, y=0, relwidth=1,relheight=1)

        alarm_btn_text = StringVar() 
        alarm_btn_text.set("Alarm")
        alarm_btn = ttk.Button(f2, textvariable=alarm_btn_text)
        alarm_btn.place(x=0, y=0, relwidth=1,relheight=1)

        alarm_name_btn_text = StringVar() 
        alarm_name_btn_text.set("No alarms")
        alarm_name_btn = ttk.Button(f3, textvariable=alarm_name_btn_text)
        alarm_name_btn.place(x=0, y=0, relwidth=1,relheight=1)

        patient_btn_text = StringVar() 
        patient_btn_text.set("Patient")
        patient_btn = ttk.Button(f4, textvariable=patient_btn_text )
        patient_btn.place(x=0, y=0, relwidth=1,relheight=1)

        switch_btn_text = StringVar() 
        switch_btn_text.set("Started")
        switch_btn = ttk.Button(f5, textvariable=switch_btn_text )
        switch_btn.place(x=0, y=0, relwidth=1,relheight=1)

        freq_btn_text = StringVar() 
        freq_btn_text.set("Frequency"+'\n'+str(self.settings.freq))
        freq_btn = ttk.Button(f7, textvariable=freq_btn_text,command = lambda: self.FreqPop(self.settings))
        freq_btn.place(x=0, y=0, relwidth=1,relheight=1)

        peep_btn_text = StringVar() 
        peep_btn_text.set("PEEP"+'\n'+str(self.settings.peep))
        peep_btn = ttk.Button(f6, textvariable=peep_btn_text )
        peep_btn.place(x=0, y=0, relwidth=1,relheight=1)

        tv_btn_text = StringVar() 
        tv_btn_text.set("Tidal Volume"+'\n'+str(self.settings.tidal_vol))
        tv_btn = ttk.Button(f10, textvariable=tv_btn_text )
        tv_btn.place(x=0, y=0, relwidth=1,relheight=1)

        pres_btn_text = StringVar() 
        pres_btn_text.set("Pressure"+'\n'+str(self.settings.pressure))
        pres_btn = ttk.Button(f11, textvariable=pres_btn_text )
        pres_btn.place(x=0, y=0, relwidth=1,relheight=1)

        oxy_btn_text = StringVar() 
        oxy_btn_text.set("Oxygen (02)"+'\n'+str(self.settings.oxygen))
        oxy_btn = ttk.Button(f12, textvariable=oxy_btn_text )
        oxy_btn.place(x=0, y=0, relwidth=1,relheight=1)


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
    #app.attributes('-fullscreen', True)
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