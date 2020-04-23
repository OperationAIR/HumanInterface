from tkinter import Button, StringVar, Tk

from utils.internationalization import Internationalization


def alarm_overview(self, settings):
    popup = Tk()
    popup.attributes('-fullscreen', True)

    Internationalization()

    popup.wm_title(_("Alarm settings"))
    popup.geometry('800x480')
    popup.configure(bg= '#161E2E')
    
        
    btn1_text = StringVar(popup)
    btn1 = Button(popup, text=_("Stop"),background='#263655',foreground='white',command=lambda: close(popup))
    btn1.config(height=15, width=15, state="normal")
    btn1.pack(side="bottom", expand = False) 


    popup.mainloop()
    return
    


def close(popup):
    popup.destroy()
    return
