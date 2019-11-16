from util import kb_global as kbg
from modules import weather_api


# Weather
class WeatherForecast(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)
        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.grid(columnspan=8, rowspan=1, sticky='NWSE')
        self.gridframe.columnconfigure((0, 1, 2, 3), weight=0)

        # warning label
        self.warning_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.s_fnt, 'normal')

        # module
        self.mod = kbg.get_config('weather_forecast')

        if weather_api.weather_data:
            day_count = self.mod[0]['config']['days']
            wd = weather_api.weather_data['daily']['data'][:day_count]
            if wd:
                self.title = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.m_fnt, 'normal')
                self.title.config(text='FORECAST')
                self.title.grid(row=0, column=0, columnspan=6, sticky='NW')
                self.divider = kbg.LineDivide(self.gridframe)
                self.divider.grid(row=1, column=0, columnspan=8, sticky='NSEW')

                self.temp_high_icon = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.s_fnt, 'normal')
                image_high = kbg.Image.open('assets/weather/temp-high-c.png')
                image_high = image_high.resize((25, 25), kbg.Image.ANTIALIAS)
                photo_high = kbg.ImageTk.PhotoImage(image_high)
                self.temp_high_icon.config(image=photo_high)
                self.temp_high_icon.image = photo_high
                self.temp_high_icon.grid(row=0, column=6, columnspan=1, sticky='NSEW')
                self.temp_low_icon = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.s_fnt, 'normal')
                image_low = kbg.Image.open('assets/weather/temp-low-c.png')
                image_low = image_low.resize((25, 25), kbg.Image.ANTIALIAS)
                photo_low = kbg.ImageTk.PhotoImage(image_low)
                self.temp_low_icon.config(image=photo_low)
                self.temp_low_icon.image = photo_low
                self.temp_low_icon.grid(row=0, column=7, columnspan=1, sticky='NSEW')

                self.daylist, self.iconlist, self.high_templist, self.low_templist = [], [], [], []
                self.icon = ''

                self.day_frame = kbg.tk.Frame(self.gridframe, bg=kbg.PRIMARY)
                self.high_temp_frame = kbg.tk.Frame(self.gridframe, bg=kbg.PRIMARY)
                self.low_temp_frame = kbg.tk.Frame(self.gridframe, bg=kbg.PRIMARY)
                self.icons_frame = kbg.tk.Frame(self.gridframe, bg=kbg.PRIMARY)

                self.set_forecast(wd)
        else:
            if weather_api.weather_error:
                cde = weather_api.weather_error['code']
                err = weather_api.weather_error['error']
                msg = f'DARKSKY API ERROR. - {cde} : {err}'
            else:
                msg = 'DARKSKY API ERROR -u'
            self.warning_lbl.grid(row=0, column=0, columnspan=4, sticky=(kbg.tk.NE, kbg.tk.S, kbg.tk.E, kbg.tk.W))
            self.warning_lbl.config(text=msg)
            print(f'[!][!] WEATHER FORECAST WIDEGET ERROR')

    def set_forecast(self, f):
        for cast in f:
            timestamp = cast['time']
            cast_datetime = kbg.datetime.datetime.fromtimestamp(timestamp)
            if cast_datetime.date() == kbg.datetime.datetime.now().date():
                short_day = 'Today'
            else:
                short_day = cast_datetime.strftime('%a')

            high_temp = f"{cast['temperatureHigh']} °c"
            low_temp = f"{cast['temperatureLow']} °c"
            icon = cast['icon']

            self.daylist.append(short_day)
            self.iconlist.append(icon)
            self.high_templist.append(high_temp)
            self.low_templist.append(low_temp)

        self.display_forecast()

    def display_forecast(self):
        self.make_text_list(self.daylist, self.day_frame, 'Poppins SemiBold')
        self.day_frame.grid(row=3, column=0, sticky='nw')
        self.make_image_list(self.iconlist)
        self.icons_frame.grid(row=3, column=5, sticky='wens', padx=(20, 20))
        self.make_text_list(self.high_templist, self.high_temp_frame, 'Poppins')
        self.high_temp_frame.grid(row=3, column=6, sticky='e', padx=(0, 20))
        self.make_text_list(self.low_templist, self.low_temp_frame, 'Poppins')
        self.low_temp_frame.grid(row=3, column=7, sticky='e')

    @staticmethod
    def make_text_list(list_arr, frame, fnt):
        for i in list_arr:
            lbl = kbg.GridLabel(frame, fnt, kbg.s_fnt, 'normal', anchor='w')
            lbl.config(text=i)
            lbl.pack(fill=kbg.tk.BOTH, expand=1, pady=(7, 3))

    def make_image_list(self, list_arr):
        icons = kbg.weather_icons()

        icon_swap = None
        for i in list_arr:
            if i in icons:
                icon_swap = icons[i]

            if icon_swap is not None:
                self.icon = icon_swap
                image = kbg.Image.open(icon_swap)
                image = image.resize((25, 25), kbg.Image.ANTIALIAS)
                photo = kbg.ImageTk.PhotoImage(image)
                lbl = kbg.GridLabel(self.icons_frame, 'Poppins', kbg.s_fnt, 'normal')
                lbl.config(image=photo)
                lbl.image = photo
                lbl.pack(fill=kbg.tk.BOTH, expand=1)
