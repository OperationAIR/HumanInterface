'''GUI to respiratory module by Jeffrey Visser '''

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import sendCommand
## for plotting
from time import sleep
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial

from settings import Settings
#global variables (maybe Dictionary)
valuePEEP = 0
valueFreq = 0
valueTida = 0
valuePres = 0
valueO2 = 0

MaxPres = 0
MinPres = 0
MaxTV = 0
MinTV = 0
MaxFi = 0
MinFi = 0

def helloCallBack():
    messagebox.showinfo( "Warning", "Warning, You stop the machinal ventilation")

def giveAlarm():
    print("alarm!!")

def getValues(): #Maybe replace to function.py if Dict
    global valuePEEP
    global valueFreq
    global valueTida
    global valuePres
    global valueO2
    valuePEEP = 5
    lbl11.configure(text= str(valuePEEP))
    valueFreq = 25
    lbl21.configure(text= str(valueFreq))
    valueTida = 200
    lbl31.configure(text= str(valueTida))
    valuePres = 30
    lbl41.configure(text= str(valuePres))
    valueO2 = 40


def saveAlarm(sendtype, settings):
    global MaxPres
    global MinPres
    global MaxTV
    global MinTV
    global MaxFi
    global MinFi

    if sendtype == "MaxP":
        MaxPres = settings.max_pressure
    elif sendtype == "MinP":
        MinPres = settings.min_pressure
    elif sendtype == "MaxT":
        MaxTV = settings.max_tv
    elif sendtype == "MinT":
        MinTV = settings.min_tv
    elif sendtype == "MaxF":
        MaxFi = settings.max_fio2
    elif sendtype == "MinF":
        MinFi = settings.min_fio2
    else:
        print("fout")

def checkAllAlarms():
    getValues()
    ser = serial.Serial ("/dev/ttyACM0", 115200, timeout=1)    #Open port with baud rate
    ser.flushInput()
    ser.write(b'p')

    if valuePEEP > MaxPres:
        lbl5.configure(foreground="red")
        giveAlarm()
    else:
        lbl5.configure(foreground="black")

    if valuePEEP < MinPres:
        lbl6.configure(foreground="red")
        giveAlarm()
    else:
        lbl6.configure(foreground="black")

    if valueTida > MaxTV:
        lbl7.configure(foreground="red")
        giveAlarm()
    else:
        lbl7.configure(foreground="black")

    if valueTida < MinTV:
        lbl8.configure(foreground="red")
        giveAlarm()
    else:
        lbl8.configure(foreground="black")

    if valueO2 > MaxFi:
        lbl9.configure(foreground="red")
        giveAlarm()
    else:
        lbl9.configure(foreground="black")

    if valueO2 < MinFi:
        lbl10.configure(foreground="red")
        giveAlarm()
    else:
        lbl10.configure(foreground="black")
    window.after(1000,checkAllAlarms)

def update_settings(settings, popup):
    popup.destroy()
    settings.update()

def confirm_settings(settings):
    popup = Tk()
    popup.wm_title("!")
    popup.geometry("700x380")
    label1 = ttk.Label(popup, text="Nieuwe instellingen:", font=("Helvetica", 20))
    label1.pack(side="top", fill="x", pady=10)

    label1 = ttk.Label(popup, text="PEEP: " + str(settings.peep), font=("Helvetica", 20))
    label1.pack(side="top", fill="x")
    label2 = ttk.Label(popup, text="Frequency [per min]: " + str(settings.freq), font=("Helvetica", 20))
    label2.pack(side="top", fill="x")
    label3 = ttk.Label(popup, text="Tidal Volume [mL]: " + str(settings.tidal_vol), font=("Helvetica", 20))
    label3.pack(side="top", fill="x")
    label4 = ttk.Label(popup, text="Pressure [cm-H2O]: " + str(settings.pressure), font=("Helvetica", 20))
    label4.pack(side="top", fill="x")

    label5 = ttk.Label(popup, text="Max Pressure Alarm [cm-H2O]: " + str(settings.max_pressure), font=("Helvetica", 20))
    label5.pack(side="top", fill="x")
    label6 = ttk.Label(popup, text="Min Pressure Alarm [cm-H2O]: " + str(settings.min_pressure), font=("Helvetica", 20))
    label6.pack(side="top", fill="x")
    label7 = ttk.Label(popup, text="Max TV alarm [mL]: " + str(settings.max_tv), font=("Helvetica", 20))
    label7.pack(side="top", fill="x")
    label8 = ttk.Label(popup, text="Min TV alarm [mL]: " + str(settings.min_tv), font=("Helvetica", 20))
    label8.pack(side="top", fill="x")
    label9 = ttk.Label(popup, text="Max fiO2 alarm [%]: " + str(settings.max_fio2), font=("Helvetica", 20))
    label9.pack(side="top", fill="x")
    label10 = ttk.Label(popup, text="Min fiO2 alarm [%]: " + str(settings.min_fio2), font=("Helvetica", 20))
    label10.pack(side="top", fill="x")

    cancel_button = ttk.Button(popup, text="CANCEL", command = popup.destroy)
    cancel_button.config(width=40)
    cancel_button.place(x=0,y=320)
    confirm_button = ttk.Button(popup, text="OK", command = lambda: update_settings(settings, popup))
    confirm_button.config(width=40)
    confirm_button.place(x=350,y=320)
    popup.mainloop()
    return

def pressurePlot():

    ser = serial.Serial ("/dev/ttyACM0", 115200, timeout=1)    #Open port with baud rate
    ser.flushInput()
    ser.write(b'p')
    # Parameters
    x_len = 200         # Number of points to display
    y_range = [0, 30]  # Range of possible Y values to display

    # Create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = list(range(0, 200))
    ys = [0] * x_len
    ax.set_ylim(y_range)

    # Create a blank line. We will update the line in animate
    line, = ax.plot(xs, ys)

    # Add labels
    plt.title('Pressure over Time')
    plt.xlabel('Samples')
    plt.ylabel('Pressure (mbar)')
    sleep(0.01)
    #window.after(1000,pressurePlot)
    # This function is called periodically from FuncAnimation
    def animate(i, ys):

        # Read temperature (Celsius) from TMP102
        try:
            pr = ser.readline().decode('utf-8').rstrip()
        except:
            pr = 0
        #print(pr)

        try:
            pressure = round(float(pr), 2)
        except ValueError:
            pressure = 0

        # Add y to list
        ys.append(pressure)

        # Limit y list to set number of items
        ys = ys[-x_len:]

        # Update line with new Y values
        line.set_ydata(ys)

        return line,

    # Set up plot to call animate() function periodically
    canvas = FigureCanvasTkAgg(fig, master=tab2)
    canvas.get_tk_widget().place(x=10,y=10)
    ani = animation.FuncAnimation(fig, animate, fargs=(ys,), interval=50, blit=True)
    #plt.show()

    #print("Alarms checked")
    window.after(1000,checkAllAlarms)

window = Tk()
window.title('Project AIR')
window.geometry('800x480')

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control) #buttons
tab2 = ttk.Frame(tab_control) #graphs
tab_control.add(tab1, text='Settings')
tab_control.add(tab2, text='Graphs')

#tab 1 Settings
btn_start = Button(tab1, text='START')
btn_stop = Button(tab1, text='STOP', command= helloCallBack)
btn_start.place(x=0,y=0)
btn_stop.place(x=70,y=0)

image = PhotoImage(file="logo.png")
label = Label(tab1, image=image)
label.place(x=460,y=50)

settings = Settings(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

lbl1 = Label(tab1, text= 'PEEP [cm-H20]')
lbl1.place(x=50,y=50)
combo1 = ttk.Combobox(tab1)
combo1['values']= (5, 10, 15, 20, 25)
combo1.set(5)
combo1.place(x=200,y=50)
lbl11 = Label(tab1, text= str(valuePEEP))
lbl11.place(x=410,y=50)

lbl2 = Label(tab1, text= 'Frequency [per min]')
lbl2.place(x=50,y=80)
combo2 = ttk.Combobox(tab1)
combo2['values']= (10, 15, 20, 25, 30, 35)
combo2.set(10)
combo2.place(x=200,y=80)
lbl21 = Label(tab1, text= str(valueFreq))
lbl21.place(x=410,y=80)

lbl3 = Label(tab1, text= 'Tidal Volume [mL]')
lbl3.place(x=50,y=110)
combo3 = ttk.Combobox(tab1)
combo3['values']= (100, 200, 300, 400, 500, 600, 700, 800)
combo3.set(100)
combo3.place(x=200,y=110)
lbl31 = Label(tab1, text= str(valueTida))
lbl31.place(x=410,y=110)

lbl4 = Label(tab1, text= 'Pressure [cm-H20]')
lbl4.place(x=50,y=140)
combo4 = ttk.Combobox(tab1)
combo4['values']= (10, 15, 20, 25, 30, 35)
combo4.set(10)
combo4.place(x=200,y=140)
lbl41 = Label(tab1, text= str(valuePres))
lbl41.place(x=410,y=140)

lbl5 = Label(tab1, text= 'Max Pressure alarm [cm-H20]')
lbl5.place(x=10,y=200)
combo5 = ttk.Combobox(tab1)
combo5['values']= (10, 20, 30, 40, 50)
combo5.set(10)
combo5.place(x=200,y=200)

lbl6 = Label(tab1, text= 'Min Pressure alarm [cm-H20]')
lbl6.place(x=10,y=230)
combo6 = ttk.Combobox(tab1)
combo6['values']= (5, 10, 15, 20, 25, 30)
combo6.set(5)
combo6.place(x=200,y=230)
combo6.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinP",get_settings()))

lbl7 = Label(tab1, text= 'Max TV alarm [mL]')
lbl7.place(x=10,y=260)
combo7 = ttk.Combobox(tab1)
combo7['values']= (100, 200, 300, 400, 500, 600, 700, 800)
combo7.set(100)
combo7.place(x=200,y=260)
combo7.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxT",get_settings()))

lbl8 = Label(tab1, text= 'Min TV alarm [mL]')
lbl8.place(x=10,y=290)
combo8 = ttk.Combobox(tab1, textvariable=100)
combo8['values']= (100, 150, 200, 250, 300)
combo8.set(100)
combo8.place(x=200,y=290)
combo8.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinT",get_settings()))

lbl9 = Label(tab1, text= 'Max fiO2 alarm [%]')
lbl9.place(x=10,y=320)
combo9 = ttk.Combobox(tab1)
combo9['values']= (40, 50, 60, 70, 80)
combo9.set(40)
combo9.place(x=200,y=320)
combo9.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxF",get_settings()))

lbl10 = Label(tab1, text= 'Min fiO2 alarm [%]')
lbl10.place(x=10,y=350)
combo10 = ttk.Combobox(tab1)
combo10['values']= (20, 35, 40, 45)
combo10.set(20)
combo10.place(x=200,y=350)
combo10.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("minF", get_settings()))

def get_settings():
    return Settings(combo1.get(), combo2.get(), combo3.get(), combo4.get(), combo5.get(), combo6.get(), combo7.get(), combo8.get(), combo9.get(), combo10.get())

confirm_settings_btn = Button(tab1, text="UPDATE", command=lambda: confirm_settings(get_settings()))
confirm_settings_btn.config(height=5, width=20, state="normal")
confirm_settings_btn.place(x=450, y = 250)


#tab 2 Graphs
# lbl2 = Label(tab2, text= 'PT Curve')
# lbl2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

checkAllAlarms()
pressurePlot()
window.mainloop()
