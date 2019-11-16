from util import kb_global as kbg
import spotipy
import spotipy.util as util


# Spotify
class Spotify(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)

        # Config
        self.mod_config = kbg.get_config('spotify')
        self.client_id = self.mod_config[0]['config']['client_id']
        self.client_secret = self.mod_config[0]['config']['client_secret']
        self.username = self.mod_config[0]['config']['username']
        self.redirect_url = 'http://google.com/'
        self.scope = 'user-library-read user-read-currently-playing user-read-playback-state'

        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.columnconfigure((0, 1),  weight=1)
        self.gridframe.columnconfigure(2, weight=2)
        self.gridframe.grid(columnspan=3, rowspan=6, sticky='NWSE')

        # spotify logo
        self.spotify_logo = kbg.GridLabel(self.gridframe, 'Poppins', kbg.s_fnt, 'normal')

        # Spotify Title
        self.title = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.m_fnt, 'normal')
        self.divider = kbg.LineDivide(self.gridframe)

        # Icon Labels
        self.artist_icon = self.make_label()
        self.track_icon = self.make_label()
        self.album_icon = self.make_label()
        self.play_icon = self.make_label()

        # labels
        self.track_name_lbl = self.make_label()
        self.artists_lbl = self.make_label()
        self.album_lbl = self.make_label()
        self.track_times_lbl = self.make_label()
        self.track_image_lbl = self.make_label()
        self.device_name_lbl = self.make_label()

        # text for labels
        self.device_name = kbg.tk.StringVar()
        self.track_name = kbg.tk.StringVar()
        self.artists = kbg.tk.StringVar()
        self.album = kbg.tk.StringVar()
        self.track_duration = kbg.tk.StringVar()
        self.track_progress = kbg.tk.StringVar()
        self.track_times = kbg.tk.StringVar()
        self.track_image = kbg.tk.StringVar()

        self.token = util.prompt_for_user_token(self.username, self.scope, client_id=self.client_id,
                                            client_secret=self.client_secret, redirect_uri=self.redirect_url)
        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            self.currently_playing()
        else:
            print("Can't get token for", self.username)
            self.display_spotfiy_logo()

    def currently_playing(self):
        results = self.sp.current_playback()
        if not results:  # if not results or not results['is_playing'] or not results['item']:
            self.remove_labels()
            self.display_spotfiy_logo()
        else:
            self.remove_spotfiy_logo()
            self.title_and_icons()
            self.device_name.set(kbg.truncate_str(f"\U000029BF {results['device']['name']}", 25))
            self.track_name.set(kbg.truncate_str(results['item']['name'], 30))
            self.artists.set(results['item']['artists'][0]['name'])
            self.album.set(kbg.truncate_str(results['item']['album']['name'], 30))
            self.track_image.set(results['item']['album']['images'][0]['url'])
            track_progress = kbg.convert_to_readable_time(results['progress_ms'])
            track_duration = kbg.convert_to_readable_time(results['item']['duration_ms'])
            self.track_times.set(f'{track_progress} / {track_duration}')

            self.add_track_labels(self.track_name_lbl, self.track_name, 2, 1, 'w', columnspan=1)
            self.add_track_labels(self.artists_lbl, self.artists, 3, 1, 'w', columnspan=1)
            self.add_track_labels(self.album_lbl, self.album, 4, 1, 'w', columnspan=1)
            self.add_track_labels(self.track_times_lbl, self.track_times, 5, 1, 'w', columnspan=1)
            self.add_track_labels(self.device_name_lbl, f'{self.device_name}', 0, 1, 'e', columnspan=2)

            image = kbg.Image.open(kbg.urlopen(self.track_image.get()))
            image = image.resize((125, 125), kbg.Image.ANTIALIAS)
            photo = kbg.ImageTk.PhotoImage(image)
            self.track_image_lbl.config(image=photo)
            self.track_image_lbl.image = photo
            self.track_image_lbl.grid(row=2, column=2, rowspan=4, sticky='ne', padx=(10, 0))
        self.after(100, self.currently_playing)

    # Add Labels
    def make_label(self):
        return kbg.GridLabel(self.gridframe, 'Poppins', kbg.xs_fnt, 'normal')

    # Add Label Icons
    def label_icons(self, icon_type, row):
        if icon_type == 'artist':
            lbl = self.artist_icon
            icon_path = kbg.os_path('assets/spotify/user.png')
        elif icon_type == 'track':
            lbl = self.track_icon
            icon_path = kbg.os_path('assets/spotify/music-player.png')
        elif icon_type == 'album':
            lbl = self.album_icon
            icon_path = kbg.os_path('assets/spotify/folder.png')
        elif icon_type == 'duration':
            lbl = self.play_icon
            icon_path = kbg.os_path('assets/spotify/pause-two-lines.png')
        else:
            lbl = ''
            icon_path = ''

        image = kbg.Image.open(icon_path)
        image = image.resize((15, 15), kbg.Image.ANTIALIAS)
        photo = kbg.ImageTk.PhotoImage(image)
        lbl.config(image=photo)
        lbl.image = photo
        lbl.grid(row=row, column=0, sticky='nw', pady=(5, 0), padx=(0, 10))

    # Add Title Bar and Icons
    def title_and_icons(self):
        # set title
        self.title.config(text='SPOTIFY')
        self.title.grid(row=0, column=0, columnspan=2, sticky='nw')
        self.divider.grid(row=1, column=0, columnspan=3, sticky='NSEW', pady=(0, 10))
        # set icons
        self.label_icons('track', 2)
        self.label_icons('artist', 3)
        self.label_icons('album', 4)
        self.label_icons('duration', 5)

    # Add Track Details To Grid
    @staticmethod
    def add_track_labels(lbl, txt, row, col, position, **kwargs):
        lbl.config(textvariable=txt, width=30, anchor=position)
        lbl.grid(row=row, column=col, sticky=position, **kwargs)

    # Remove Labels
    def remove_labels(self):
        self.title.grid_forget()
        self.divider.grid_forget()
        self.artist_icon.grid_forget()
        self.track_icon.grid_forget()
        self.album_icon.grid_forget()
        self.play_icon.grid_forget()
        self.track_name_lbl.grid_forget()
        self.artists_lbl.grid_forget()
        self.album_lbl.grid_forget()
        self.track_times_lbl.grid_forget()
        self.track_image_lbl.grid_forget()
        self.device_name_lbl.grid_forget()

    def display_spotfiy_logo(self):
        image = kbg.Image.open(kbg.os.path.join(kbg.os.path.dirname(kbg.sys.executable), 'assets/spotify/spotify.png'))
        photo = kbg.ImageTk.PhotoImage(image)
        self.spotify_logo.config(image=photo)
        self.spotify_logo.image = photo
        self.spotify_logo.grid(row=0, column=0, sticky='NWSE')

    def remove_spotfiy_logo(self):
        self.spotify_logo.grid_forget()
