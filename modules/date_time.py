from util import kb_global as kbg


class DateTime(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)
        # grid
        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.grid(columnspan=1, rowspan=1)
        self.gridframe.columnconfigure(0, weight=1)
        self.gridframe.rowconfigure(0, weight=0)

        # time
        self.date_time = kbg.datetime.datetime.now()
        self.time_string_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.xl_fnt, 'normal', anchor='nw')
        self.locale_string_lbl = kbg.GridLabel(self.gridframe, 'Poppins Light', kbg.l_fnt, 'normal', anchor='nw')
        self.time_string = kbg.tk.StringVar()
        self.locale_string = kbg.tk.StringVar()

        # long full date
        self.date_string_lbl = kbg.GridLabel(self.gridframe, 'Poppins Light', kbg.m_fnt, 'normal', anchor='nw')
        self.date_string = kbg.tk.StringVar()

        # grid
        self.date_string_lbl.grid(row=0, column=0, sticky='nw', columnspan=2)
        self.time_string_lbl.grid(row=0, column=0, sticky='nw', pady=(0, 0), columnspan=1)
        self.locale_string_lbl.grid(row=0, column=1, sticky='nw', pady=(75, 0), padx=(0, 0), columnspan=1)

        self.set_date()
        self.set_time()

    def set_time(self, time1=''):
        time2 = kbg.time.strftime("%H:%M")
        if time2 != time1:
            time1 = time2
        self.time_string.set(time2)
        self.locale_string.set(kbg.time.strftime("%p"))
        self.date_string_lbl.config(text=self.date_string.get())
        self.time_string_lbl.config(text=self.time_string.get())
        self.locale_string_lbl.config(text=self.locale_string.get())
        self.gridframe.after(200, self.set_time)

    def set_date(self):
        n_time = kbg.datetime.datetime.now()
        # date
        date_string = str(n_time.strftime("%A") + ' ' + n_time.strftime("%d") + ' ' + n_time.strftime("%B"))
        self.date_string.set(date_string)
