'''GUI to respiratory module by Jeffrey Visser '''

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functions import sendCommand

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
    valueFreq = 25
    valueTida = 600
    valuePres = 30
    valueO2 = 70

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
        lbl5.configure(foreground="red")
        giveAlarm()
    else:
        lbl5.configure(foreground="black")   
    print("Alarms checked")
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
combo1['values']= (1, 2, 3, 4, 5)
combo1.place(x=200,y=50)
combo1.bind("<<ComboboxSelected>>", lambda _ : sendCommand("PEEP",combo1.get()))
lbl11 = Label(tab1, text= str(valuePEEP))
lbl11.place(x=410,y=50)

lbl2 = Label(tab1, text= 'Frequency [per min]')
lbl2.place(x=50,y=80)
combo2 = ttk.Combobox(tab1)
combo2['values']= (1, 20, 3, 4, 5)
combo2.place(x=200,y=80)
combo2.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Freq",combo2.get()))
lbl21 = Label(tab1, text= str(valueFreq))
lbl21.place(x=410,y=80)

lbl3 = Label(tab1, text= 'Tidal Volume [mL]')
lbl3.place(x=50,y=110)
combo3 = ttk.Combobox(tab1)
combo3['values']= (1, 2, 300, 4, 5)
combo3.place(x=200,y=110)
combo3.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Tida",combo3.get()))
lbl31 = Label(tab1, text= str(valueTida))
lbl31.place(x=410,y=110)

lbl4 = Label(tab1, text= 'Pressure [cm-H20]')
lbl4.place(x=50,y=140)
combo4 = ttk.Combobox(tab1)
combo4['values']= (1, 20, 3, 4, 5)
combo4.place(x=200,y=140)
combo4.bind("<<ComboboxSelected>>", lambda _ : sendCommand("Pres",combo4.get()))
lbl41 = Label(tab1, text= str(valuePres))
lbl41.place(x=410,y=140)

lbl5 = Label(tab1, text= 'Max Pressure alarm [cm-H20]')
lbl5.place(x=10,y=200)
combo5 = ttk.Combobox(tab1)
combo5['values']= (1, 2, 30, 4, 5)
combo5.place(x=200,y=200)
combo5.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxP",combo5.get()))

lbl6 = Label(tab1, text= 'Min Pressure alarm [cm-H20]')
lbl6.place(x=10,y=230)
combo6 = ttk.Combobox(tab1)
combo6['values']= (15, 2, 30, 4, 5)
combo6.place(x=200,y=230)
combo6.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinP",combo6.get()))

lbl7 = Label(tab1, text= 'Max TV alarm [mL]')
lbl7.place(x=10,y=260)
combo7 = ttk.Combobox(tab1)
combo7['values']= (1, 2, 350, 4, 20)
combo7.place(x=200,y=260)
combo7.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxT",combo7.get()))

lbl8 = Label(tab1, text= 'Min TV alarm [mL]')
lbl8.place(x=10,y=290)
combo8 = ttk.Combobox(tab1)
combo8['values']= (1, 250, 3, 4, 20)
combo8.place(x=200,y=290)
combo8.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MinT",combo8.get()))

lbl9 = Label(tab1, text= 'Max fiO2 alarm [%]')
lbl9.place(x=10,y=320)
combo9 = ttk.Combobox(tab1)
combo9['values']= (1, 2, 30, 4, 50)
combo9.place(x=200,y=320)
combo9.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("MaxF",combo9.get()))

lbl10 = Label(tab1, text= 'Min fiO2 alarm [%]')
lbl10.place(x=10,y=350)
combo10 = ttk.Combobox(tab1)
combo10['values']= (1, 20, 3, 4, 50)
combo10.place(x=200,y=350)
combo10.bind("<<ComboboxSelected>>", lambda _ : saveAlarm("minF",combo10.get()))

#tab 2 Graphs
lbl2 = Label(tab2, text= 'PT Curve')
lbl2.grid(column=0, row=0)


tab_control.pack(expand=1, fill='both')

checkAllAlarms()
window.mainloop()
