# Global Imports,  Variables and Functions
import logging
import os
import sys
import tkinter as tk
from urllib.request import urlopen
from PIL import Image, ImageTk
import dateutil
from dateutil.parser import *
import datetime
import timeago
import time
import requests
import json
import webbrowser


# Colours and Font Sizes
PRIMARY = '#0F0F0F'
SECONDARY = '#000000'
WHITE = '#F0F0F0'
xl_fnt = 80
l_fnt = 30
md_fnt = 20
m_fnt = 16
s_fnt = 13
xs_fnt = 12
xxs_fnt = 10


# JSON PRETTY PRINT
def json_print(j):
    return print(json.dumps(j, indent=4, sort_keys=True))


# connection check
def connectivity():
    try:
        requests.get('https://www.google.com/', timeout=10)
        return True
    except requests.ConnectionError:
        print('internet connection down')
        return False


# Get config.json
def config():
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data


# Get An Individual Active Module Config
def get_config(mod_name):
    conf = config()
    modules = conf['modules']
    mod = list(filter(lambda elem: elem['module'] == mod_name and elem['active'] is True, modules))
    return mod


# Grid Labels
class GridLabel(tk.Label):
    def __init__(self, master, fnt, fnt_size, fnt_weight, **kwargs):
        self.fnt = fnt
        self.fnt_size = fnt_size
        self.fnt_weight = fnt_weight
        tk.Label.__init__(self, master, bd=0, fg=WHITE,
                          bg=PRIMARY, font=(self.fnt, self.fnt_size, self.fnt_weight), **kwargs)


# Line Divider
class LineDivide(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg=WHITE, height=2)


# os path for assets
def os_path(path):
    pth = os.path.join(os.path.dirname(sys.executable), path)
    return pth


# Config Lists
def list_config(listbox, fnt, fnt_size, **kwargs):
    return listbox.config(bg=PRIMARY, fg=WHITE, borderwidth=0, activestyle='none', bd=0, highlightthickness=0,
                          selectbackground=PRIMARY, **kwargs, font=(fnt, fnt_size, 'normal'))


# Weather Icons
def weather_icons():
    fetch_icons = {
        'clear-day': os_path("assets/weather/clear-day-c.png"),  # clear sky day
        'clear-night': os_path("assets/weather/clear-night-c.png"),  # clear sky night
        'wind': os_path("assets/weather/wind-c.png"),  # wind
        'cloudy': os_path("assets/weather/cloudy-c.png"),  # cloudy day
        'partly-cloudy-day': os_path("assets/weather/cloudy-day-c.png"),  # partly cloudy day
        'partly-cloudy-night': os_path("assets/weather/cloudy-night-c.png"),  # scattered clouds night
        'rain': os_path("assets/weather/rain-c.png"),  # rain day
        'snow': os_path("assets/weather/snow-c.png"),  # snow day
        'snow-thin': os_path("assets/weather/snow-c.png"),  # snow/sleet day
        'fog': os_path("assets/weather/fog-c.png"),  # fog day
        'thunderstorm': os_path("assets/weather/storm-c.png"),  # thunderstorm
        'tornado': os_path("assets/weather/tornado-c.png"),  # tornado
        'hail': os_path("assets/weather/hail-c.png")  # hail
    }

    return fetch_icons


# Truncate strings
def truncate_str(string, length=20):
    truncated = (string[:length] + '...') if len(string) > length else string
    return truncated


# Convert Milliseconds
def convert_to_readable_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = seconds + milliseconds / 1000

    if int(seconds) < 10:
        seconds = f'0{int(seconds)}'
    else:
        seconds = int(seconds)

    if days >= 1:
        return f'{days} day:{hours} hrs:{minutes}:{seconds}'
    elif not days >= 1:
        if hours >= 1:
            return f'{hours}:{minutes}:{seconds}'
        else:
            return f'{minutes}:{seconds}'