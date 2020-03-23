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


def saveAlarm(sendtype, sendvalue):
    global MaxPres
    global MinPres
    global MaxTV
    global MinTV
    global MaxFi
    global MinFi

    if sendtype == "MaxP":
        MaxPres = int(sendvalue)
    elif sendtype == "MinP":
        MinPres = int(sendvalue)
    elif sendtype == "MaxT":
        MaxTV = int(sendvalue)
    elif sendtype == "MinT":
        MinTV = int(sendvalue)
    elif sendtype == "MaxF":
        MaxFi = int(sendvalue)
    elif sendtype == "MinF":
        MinFi = int(sendvalue)    
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
        print(pr)
        
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
    plt.show()
    
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
btn_stop.place(x=50,y=0)

image = PhotoImage(file="logo.png")
label = Label(tab1, image=image)
label.place(x=460,y=50)

lbl1 = Label(tab1, text= 'PEEP [cm-H20]')
lbl1.place(x=50,y=50)
combo1 = ttk.Combobox(tab1)
combo1['values']= (5, 10, 15, 20, 25)
combo1.place(x=200,y=50)
combo1.bind("<<ComboboxSelected>>", lambda _ : sendCommand("PEEP",combo1.get()))
lbl11 = Label(tab1, text= str(valuePEEP))
lbl11.place(x=410,y=50)

lbl2 = Label(tab1, text= 'Frequency [per min]')
lbl2.place(x=50,y=80)
combo2 = ttk.Combobox(tab1)
combo2['values']= (10, 15, 20, 25, 30, 35)
combo2.place(x=200,y=80)
combo2.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Freq",combo2.get()))
lbl21 = Label(tab1, text= str(valueFreq))
lbl21.place(x=410,y=80)

lbl3 = Label(tab1, text= 'Tidal Volume [mL]')
lbl3.place(x=50,y=110)
combo3 = ttk.Combobox(tab1)
combo3['values']= (100, 200, 300, 400, 500, 600, 700, 800)
combo3.place(x=200,y=110)
combo3.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Tida",combo3.get()))
lbl31 = Label(tab1, text= str(valueTida))
lbl31.place(x=410,y=110)

lbl4 = Label(tab1, text= 'Pressure [cm-H20]')
lbl4.place(x=50,y=140)
combo4 = ttk.Combobox(tab1)
combo4['values']= (10, 15, 20, 25, 30, 35)
combo4.place(x=200,y=140)
combo4.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Pres",combo4.get()))
lbl41 = Label(tab1, text= str(valuePres))
lbl41.place(x=410,y=140)

lbl5 = Label(tab1, text= 'Max Pressure alarm [cm-H20]')
lbl5.place(x=10,y=200)
combo5 = ttk.Combobox(tab1)
combo5['values']= (10, 20, 30, 40, 50)
combo5.place(x=200,y=200)
combo5.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxP",combo5.get()))

lbl6 = Label(tab1, text= 'Min Pressure alarm [cm-H20]')
lbl6.place(x=10,y=230)
combo6 = ttk.Combobox(tab1)
combo6['values']= (5, 10, 15, 20, 25, 30)
combo6.place(x=200,y=230)
combo6.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinP",combo6.get()))

lbl7 = Label(tab1, text= 'Max TV alarm [mL]')
lbl7.place(x=10,y=260)
combo7 = ttk.Combobox(tab1)
combo7['values']= (100, 200, 300, 400, 500, 600, 700, 800)
combo7.place(x=200,y=260)
combo7.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxT",combo7.get()))

lbl8 = Label(tab1, text= 'Min TV alarm [mL]')
lbl8.place(x=10,y=290)
combo8 = ttk.Combobox(tab1)
combo8['values']= (100, 150, 200, 250, 300)
combo8.place(x=200,y=290)
combo8.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinT",combo8.get()))

lbl9 = Label(tab1, text= 'Max fiO2 alarm [%]')
lbl9.place(x=10,y=320)
combo9 = ttk.Combobox(tab1)
combo9['values']= (40, 50, 60, 70, 80)
combo9.place(x=200,y=320)
combo9.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxF",combo9.get()))

lbl10 = Label(tab1, text= 'Min fiO2 alarm [%]')
lbl10.place(x=10,y=350)
combo10 = ttk.Combobox(tab1)
combo10['values']= (20, 35, 40, 45)
combo10.place(x=200,y=350)
combo10.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("minF",combo10.get()))

#tab 2 Graphs
lbl2 = Label(tab2, text= 'PT Curve')
lbl2.grid(column=0, row=0)


tab_control.pack(expand=1, fill='both')

checkAllAlarms()
pressurePlot()
window.mainloop()
