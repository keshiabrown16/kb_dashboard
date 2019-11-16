# -*- coding: utf-8 -*-
import importlib
import concurrent.futures
from util import kb_global as kbg


# If either weather widgets are added, get the data - so we only make the call once
if kbg.get_config('current_weather') or kbg.get_config('weather_forecast'):
    from modules import weather_api
    weather_api.get()


class Grid(kbg.tk.Frame):
    def __init__(self, master):
        # TK
        kbg.tk.Frame.__init__(self, master)
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.master.configure(background=kbg.PRIMARY, padx=40, pady=40)
        self.master.columnconfigure((0, 1, 2), weight=1)
        self.master.rowconfigure((0, 2), weight=0)
        self.master.rowconfigure(1, weight=2)

        # Fullscreen Toggle
        self.state = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        # Top Frame
        self.topframe = kbg.tk.Frame(self.master, bg=kbg.PRIMARY, height=160)
        self.topframe.rowconfigure(0, weight=0)
        self.topframe.grid_propagate(0)
        self.topframe.grid(row=0, column=0, columnspan=3, rowspan=1, sticky='NSEW')

        # Mid Frame
        self.midframe = kbg.tk.Frame(self.master, bg=kbg.PRIMARY)
        self.midframe.rowconfigure(0, weight=0)
        self.midframe.columnconfigure((0, 1, 2), weight=0)
        self.midframe.grid(row=1, column=0, columnspan=3, rowspan=2, sticky='NSEW', pady=(25, 0))

        # Bottom Frame
        self.bottomframe = kbg.tk.Frame(self.master, bg=kbg.PRIMARY)
        self.bottomframe.rowconfigure(0, weight=0)
        self.bottomframe.rowconfigure(1, weight=1)
        self.bottomframe.columnconfigure(0, weight=1)
        self.bottomframe.grid(row=2, column=0, columnspan=3, rowspan=2, sticky='NSEW')

        # get active widget modules
        conf = kbg.config()
        active_mods = list(filter(lambda elem: elem['active'] is True, conf['modules']))

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            print(f"started at {kbg.time.strftime('%X')}")
            x = {executor.submit(self.load_module(mod['module'])): mod for mod in active_mods}
            for future in concurrent.futures.as_completed(x):
                m = x[future]
                try:
                    n = future.running
                except Exception as exc:
                    print('%r generated an exception: %s' % (m, exc))
                else:
                    self.pack_modules()
            print(f"ended at {kbg.time.strftime('%X')}")

    def load_module(self, module):
        x = importlib.import_module('modules.' + module)
        self.set_mod_class(module, x)
        return x

    def set_mod_class(self, module, cls):
        if module == 'date_time':
            self.master.dt = cls.DateTime(self.topframe)
        elif module == 'current_weather':
            self.master.current_weather = cls.CurrentWeather(self.topframe)
        elif module == 'google_calendar':
            self.master.gc = cls.GoogleCalendar(self.midframe)
        elif module == 'spotify':
            self.master.spotify = cls.Spotify(self.midframe)
        elif module == 'weather_forecast':
            self.master.wfc = cls.WeatherForecast(self.midframe)
        elif module == 'news':
            self.master.news = cls.News(self.bottomframe)

    def pack_modules(self):
        try:
            self.master.dt.pack(side=kbg.tk.LEFT, fill=kbg.tk.BOTH, expand=0)
        except AttributeError as err1:
            print('%r generated an exception: %s' % ('date_time', err1))

        try:
            self.master.current_weather.pack(side=kbg.tk.RIGHT, fill=kbg.tk.BOTH, expand=0)
        except AttributeError as err2:
            print('%r generated an exception: %s' % ('current_weather', err2))

        try:
            self.master.gc.pack(side=kbg.tk.LEFT, fill=kbg.tk.BOTH, expand=1)
        except AttributeError as err3:
            print('%r generated an exception: %s' % ('google_calendar', err3))

        try:
            self.master.spotify.pack(side=kbg.tk.LEFT, fill=kbg.tk.BOTH, expand=1, anchor=kbg.tk.CENTER)
        except AttributeError as err4:
            print('%r generated an exception: %s' % ('spotify', err4))

        try:
            self.master.wfc.pack(side=kbg.tk.RIGHT, fill=kbg.tk.BOTH, expand=0)
        except AttributeError as err5:
            print('%r generated an exception: %s' % ('weather_forecast', err5))

        try:
            self.master.news.pack(side='bottom', fill=kbg.tk.Y, anchor=kbg.tk.CENTER)
        except AttributeError as err6:
            print('%r generated an exception: %s' % ('news', err6))

    # Toggle Fullscreen
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes("-fullscreen", self.state)
        return "break"

    # Exit Fullscreen
    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes("-fullscreen", False)
        return "break"


def main():
    root = kbg.tk.Tk()
    conf = kbg.config()
    root.title(conf['name'])
    root.resizable(False, False)
    win = Grid(root)
    win.tk.mainloop()


if __name__ == '__main__':
    main()
