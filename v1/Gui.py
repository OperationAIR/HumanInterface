from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def helloCallBack():
    messagebox.showinfo( "Warning", "Warning, You stop the machinal ventilation")
    
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
label.place(x=450,y=50)

lbl1 = Label(tab1, text= 'PEEP [cm-H20]')
lbl1.place(x=50,y=50)
combo1 = ttk.Combobox(tab1)
combo1['values']= (1, 2, 3, 4, 5)
combo1.place(x=200,y=50)

lbl2 = Label(tab1, text= 'Frequency [per min]')
lbl2.place(x=50,y=80)
combo2 = ttk.Combobox(tab1)
combo2['values']= (1, 2, 3, 4, 5)
combo2.place(x=200,y=80)

lbl3 = Label(tab1, text= 'Tidal Volume [mL]')
lbl3.place(x=50,y=110)
combo3 = ttk.Combobox(tab1)
combo3['values']= (1, 2, 3, 4, 5)
combo3.place(x=200,y=110)

lbl4 = Label(tab1, text= 'Pressure [cm-H20]')
lbl4.place(x=50,y=140)
combo4 = ttk.Combobox(tab1)
combo4['values']= (1, 2, 3, 4, 5)
combo4.place(x=200,y=140)

#tab 2 Graphs
lbl2 = Label(tab2, text= 'PT Curve')
lbl2.grid(column=0, row=0)


tab_control.pack(expand=1, fill='both')

window.mainloop()

