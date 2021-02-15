import tkinter as tk
import tkinter.font as font
from tkinter.messagebox import showerror
import time
import math
from datetime import datetime

euro = 0
cents = 0
hcent = 0
salaris = 0
datum_tijd = ''
logfile = open('log.txt', 'a')
stop = False
tijd1 = ''
tijd2 = ''

class Timer:
    def __init__(self):
        self.root = tk.Tk()
        self.text_variabel = tk.StringVar()
        self.root.geometry('455x300')
        self.root.resizable(False,False)
        self.root.configure(bg='lightblue')
        self.root.title('GeldStopwatch')
        self.root.iconbitmap(r'euroicon.ico')

        self.start_tijd = None
        self.is_running = False

        self.make_widgets()


        self.root.bind('<Return>', self.startstop)
        self.root.mainloop()

    def make_widgets(self):

        label1 = tk.Label(self.root, textvariable=self.text_variabel, font='ariel 30', fg='white', bg='lightblue').pack(pady=20)

        btn_frame = tk.Frame(self.root, bg='lightblue')
        btn_frame.place(relwidth=1, relheight=.6, rely=.2)
        Knop1 = tk.Button(btn_frame, text='Start', command=self.start, font=font.Font(size=25, family='Helvetica'), width=6, relief='groove', activeforeground='white', activebackground='lightgreen')
        Knop1.place(relwidth=.4,relheight=.5, relx=.05, rely=.2)
        Knop2 = tk.Button(btn_frame, text='Stop', command=self.stop, font=font.Font(size=25, family='Helvetica'), width=6, relief='groove', activeforeground='white', activebackground='salmon')
        Knop2.place(relwidth=.4, relheight=.5, relx=.55, rely=.2)

        text_frame = tk.Frame(self.root)
        text_frame.place(relwidth=.8, relheight=.1, rely=.65, relx=.1)

        self.invul_frame = tk.Frame(self.root)
        self.invul_frame.place(relwidth=.25, relheight=.15, rely=.8, relx=.225)

        invul_knop_frame = tk.Frame(self.root)
        invul_knop_frame.place(relwidth=.25, relheight=.15, relx=.525, rely=.8)

        text_label = tk.Label(text_frame, text='Vul hieronder je uurloon in!', font='Helvetica 20', bg='lightblue')
        text_label.place(relwidth=1, relheight=1)

        self.invul_entry = tk.Entry(self.invul_frame, font='Helvetica 20')
        self.invul_entry.place(relwidth=1, relheight=1)

        invul_knop = tk.Button(invul_knop_frame, text='sla op', font='Helvetica 15', command=self.check_type)
        invul_knop.place(relwidth=1, relheight=1)

    def check_type(self):
        global salaris

        try:
            input_int = self.invul_entry.get()
            float(input_int)
            salaris = float(self.invul_entry.get())
            salaris = salaris / 3600

        except ValueError:
            showerror('Error', "Gebruik alleen nummers, of nummers met een punt (7.2)  GEBRUIK GEEN LETTERS OF KOMMA'S")
            salaris = 0


    def start(self):
        global datum_tijd, logfile, tijd1

        if not self.is_running:
            logfile = open('log.txt', 'a')
            self.start_tijd = time.time()
            self.timer()
            self.is_running = True

            nu = datetime.now()
            datum_tijd = nu.strftime("%d/%m/%Y, %H:%M:%S.%f")
            logfile.write('gestart op: ' + '[' + str(datum_tijd) + ']' + '\n')
            tijd1 = datum_tijd


    def timer(self):
        self.text_variabel.set(self.format_time(time.time() - self.start_tijd))
        self.after_loop = self.root.after(50, self.timer)

    def stop(self):
        global datum_tijd, logfile, cent, stop, tijd1, tijd2

        if self.is_running:
            stop = True
            str_salaris = int(salaris) * 3600
            nu = datetime.now()
            datum_tijd = nu.strftime("%d/%m/%Y, %H:%M:%S.%f")
            tijd2 = datum_tijd
            tijdverschil = datetime.strptime(tijd2, "%d/%m/%Y, %H:%M:%S.%f") - datetime.strptime(tijd1, "%d/%m/%Y, %H:%M:%S.%f")
            logfile.write('totale tijd: ' + str(tijdverschil) + '\n')

            kommasalaris = str('€%05.3f' % (cents))
            kommasalaris = kommasalaris.replace('.', ',')
            logfile.write('totaal geld gemaakt: ' + str(kommasalaris) + '\n')

            uurloon = str(self.invul_entry.get())
            uurloon = uurloon.replace('.', ',')
            logfile.write('uurloon: ' + '€' + str(uurloon) + ' p/u' + '\n')

            logfile.write('geëindigd op: ' + '[' + str(datum_tijd) + ']' + '\n')
            logfile.write('\n')

            logfile.close()

            self.root.after_cancel(self.after_loop)
            self.is_running = False

    def startstop(self, event=None):
        if self.is_running:
            self.stop()
        else:
            self.start()

    @staticmethod
    def format_time(elap):
        global cents, hcent, euro, salaris, logfile
        hours = int(elap / 3600)
        minutes = int(elap / 60 - hours * 60.0)
        seconds = int(elap - hours * 3600.0 - minutes * 60.0)
        hseconds = int((elap - hours * 3600.0 - minutes * 60.0 - seconds) * 10)

        cents = (seconds * salaris) + (minutes * salaris)*60 + (hours * salaris)*3600
        return '%02d:%02d:%02d:%1d' % (hours, minutes, seconds, hseconds), '€%05.3f' % (cents)


Timer()