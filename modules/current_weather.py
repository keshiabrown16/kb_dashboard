from util import kb_global as kbg
from modules import weather_api


# Weather
class CurrentWeather(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)

        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.grid(columnspan=4, rowspan=1)
        self.gridframe.rowconfigure(0, weight=0)
        self.gridframe.columnconfigure((0, 1), weight=0)

        # get config
        self.wmod = kbg.get_config('current_weather')

        # warning label
        self.warning_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.s_fnt, 'normal', wraplength=400)
        conf = kbg.config()
        self.city = conf['city']
        self.country = conf['country_code']
        self.location = self.city + ', ' + self.country
        self.icon, self.icon_name = '', ''
        self.icon_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.m_fnt, 'normal')
        self.temperature_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', 40, 'normal', anchor='ne')
        self.summary_lbl = kbg.GridLabel(self.gridframe, 'Poppins Light', kbg.m_fnt, 'normal', anchor='ne')
        self.location_lbl = kbg.GridLabel(self.gridframe, 'Poppins Light', kbg.m_fnt, 'normal', anchor='ne')

        if weather_api:
            if weather_api.weather_data:
                self.display_weather(weather_api.weather_data)
            else:
                if weather_api.weather_error:
                    cde = weather_api.weather_error['code']
                    err = weather_api.weather_error['error']
                    msg = f'DARKSKY API ERROR. - {cde} : {err}'
                else:
                    msg = 'DARKSKY API ERROR'

                self.warning_lbl.grid(row=0, column=1, columnspan=4, sticky=(kbg.tk.NE, kbg.tk.S, kbg.tk.E, kbg.tk.W))
                self.warning_lbl.config(text=msg)
                print(f'[!][!] CURRENT WEATHER WIDGET ERROR')
        else:
            print('NO WEATHER API')

    def display_weather(self, w):
        icon_swap = None
        self.icon_name = w['currently']['icon']
        summary = w['currently']['summary']
        temperature = w['currently']['temperature']

        icons = kbg.weather_icons()

        if self.icon_name in icons:
            icon_swap = icons[self.icon_name]

        if icon_swap is not None:
            if self.icon != icon_swap:
                self.icon = icon_swap
                image = kbg.Image.open(icon_swap)
                image = image.resize((115, 115), kbg.Image.ANTIALIAS)
                photo = kbg.ImageTk.PhotoImage(image)

                self.icon_lbl.config(image=photo)
                self.icon_lbl.image = photo
                if self.wmod[0]['config']['icon']:
                    self.icon_lbl.grid(row=0, column=0, sticky=(kbg.tk.N, kbg.tk.S, kbg.tk.E, kbg.tk.W))
        else:
            print('no icon')

        self.location_lbl.grid(row=0, column=1, sticky="ne")
        self.location_lbl.config(text=self.location)
        self.temperature_lbl.grid(row=0, column=1, sticky="se", pady=(22, 12))
        self.temperature_lbl.config(text=f'{temperature}°C')
        self.summary_lbl.grid(row=0, column=1, sticky="se")
        self.summary_lbl.config(text=summary)
