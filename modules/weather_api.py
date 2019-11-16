from util import kb_global as kbg


# Weather Api Call
conf = kbg.config()
wconfig = conf['weather']


def get():
    a_key = wconfig['key']
    lat = wconfig['latitude']
    lon = wconfig['longitude']
    units = wconfig['units']
    exc = wconfig['exclude']
    url = f'https://api.darksky.net/forecast/{a_key}/{lat},{lon}?units={units}&exclude={exc}'

    global weather_data
    global weather_error

    try:
        req = kbg.requests.get(url, headers={'content-type': "application/json"})
    except Exception as e:
        kbg.logging.exception(e)
        print("Couldn't get weather results")
    else:
        if req.status_code == 200:
            weather_data = req.json()
            weather_error = None
        elif req.status_code >= 500:
            res = req.json()
            print('[!] WEATHER - DARKSKY - [{0}] Server Error'.format(req.status_code))
            weather_error = res
            weather_data = None
        elif req.status_code == 401:
            res = req.json()
            print(f"[!] WEATHER - DARKSKY - Permission Denied - code : {res['code']} - error: {res['error']}")
            weather_error = res
            weather_data = None
        elif req.status_code == 403:
            res = req.json()
            print(f"[!] WEATHER - DARKSKY - Exceeded API Call Limit - code: {res['code']} = error: {res['error']}")
            weather_error = res
            weather_data = None
        elif req.status_code >= 400:
            res = req.json()
            print(f"[!] WEATHER - DARKSKY - Client Error - code : {res['code']} = error: {res['error']}")
            weather_error = res
            weather_data = None
