from __future__ import print_function
from util import kb_global as kbg
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Weather
class GoogleCalendar(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)

        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.columnconfigure((0, 1, 2, 3), weight=0)
        self.gridframe.grid(columnspan=4, rowspan=1, sticky='NWSE')

        self.titleLbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.m_fnt, 'normal')
        self.titleLbl.config(text='CALENDAR')
        self.divider = kbg.LineDivide(self.gridframe)
        self.max_name_width, self.max_date_width, self.max_list_height = 0, 0, 0
        self.event_name_list = kbg.tk.Listbox(self.gridframe, bg=kbg.PRIMARY)
        self.event_date_list = kbg.tk.Listbox(self.gridframe, bg=kbg.PRIMARY)
        kbg.list_config(self.event_name_list, 'Poppins SemiBold', kbg.s_fnt)
        kbg.list_config(self.event_date_list, 'Poppins', kbg.s_fnt, justify=kbg.tk.RIGHT)

        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.creds = None
        self.mod_config = kbg.get_config('google_calendar')
        self.get_calendar()

    def get_calendar(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        service = build('calendar', 'v3', credentials=self.creds)

        # Call the Calendar API to get next 10 upcoming events
        now = kbg.datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        item_count = self.mod_config[0]['config']['item_count']
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=item_count,
                                              singleEvents=True, orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')

        for event in events:
            now = kbg.datetime.datetime.now() + kbg.datetime.timedelta(seconds=60 * 3.4)
            event_start = event['start'].get('dateTime', event['start'].get('date'))
            # converting each event start to datetime so we can work with timeago
            # this is because the google calendar api can return either date or datetime format
            convert_to_datetime = kbg.dateutil.parser.parse(event_start)
            remove_timezone = convert_to_datetime.replace(tzinfo=None)
            start = kbg.timeago.format(remove_timezone, now)

            # Add To Relevant Listbox
            self.event_name_list.insert(kbg.tk.END, kbg.truncate_str(event['summary'], 30))
            self.event_date_list.insert(kbg.tk.END, start)

            if len(events) > self.max_list_height:
                self.max_list_height = len(events)

            # Set length if listbox to longest item
            if len(event['summary']) > self.max_name_width:
                self.max_name_width = len(event['summary'])

            if len(start) > self.max_date_width:
                self.max_date_width = len(start)

        self.event_name_list.config(width=self.max_name_width - 2, height=self.max_list_height)
        self.event_date_list.config(width=self.max_date_width, height=self.max_list_height)
        self.titleLbl.grid(row=0, column=0, columnspan=4, sticky='NW')
        self.divider.grid(row=1, column=0, columnspan=4, sticky=(kbg.tk.N, kbg.tk.S, kbg.tk.E, kbg.tk.W), pady=(0, 10))
        self.event_name_list.grid(row=2, column=0, columnspan=2, sticky='nw')
        self.event_date_list.grid(row=2, column=2, columnspan=2, sticky='ne')


