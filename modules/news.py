from util import kb_global as kbg
from newsapi import NewsApiClient


# News
class News(kbg.tk.Frame):
    def __init__(self, parent):
        kbg.tk.Frame.__init__(self, parent, bg=kbg.PRIMARY)

        self.gridframe = kbg.tk.Frame(self, bg=kbg.PRIMARY)
        self.gridframe.rowconfigure(0, weight=1)
        self.gridframe.rowconfigure(1, weight=1)
        self.gridframe.columnconfigure(0, weight=3)
        self.gridframe.grid(column=0, row=0, columnspan=3, sticky='NSEW')
        # warning label
        self.warning_lbl = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.s_fnt, 'normal', wraplength=400)
        self.news_headlines = dict()
        self.headline_index = 0

        # labels
        self.published_details_label = kbg.GridLabel(self.gridframe, 'Poppins Light', kbg.xs_fnt, 'normal')
        self.title_label = kbg.GridLabel(self.gridframe, 'Poppins SemiBold', kbg.md_fnt, 'normal', wraplength=1000)

        # text
        self.headline_title, self.headline_url, self.published_details = [kbg.tk.StringVar(), kbg.tk.StringVar(),
                                                                          kbg.tk.StringVar()]

        self.get_headlines()

    def get_headlines(self):
        nconfig = kbg.get_config('news')
        newsapi = NewsApiClient(api_key=nconfig[0]['config']['key'])
        try:
            self.news_headlines = newsapi.get_top_headlines(sources=nconfig[0]['config']['sources'])
        except Exception as e:
            err = e.args[0]
            self.warning_lbl.config(text=err['message'])
            self.warning_lbl.grid(row=0, column=0)
        else:
            self.show_headlines()
            #self.gridframe.after(100000, self.get_headlines)

    def show_headlines(self):
        top_headlines = self.news_headlines
        headlines_len = len(top_headlines['articles'])
        article = top_headlines['articles'][self.headline_index]
        self.headline_index += 1

        if self.headline_index == headlines_len:
            self.headline_index = 0

        self.headline_title.set(article['title'])
        self.headline_url.set(article['url'])

        datetime_now = kbg.datetime.datetime.now()
        article_date_time = kbg.dateutil.parser.parse(article['publishedAt'])
        article_date = article_date_time.replace(tzinfo=None)
        time_from_now = kbg.timeago.format(article_date, datetime_now)
        pd = f"by {article['source']['name']}, {time_from_now}"
        self.published_details.set(pd)
        self.title_label.config(textvariable=self.headline_title)
        self.published_details_label.config(textvariable=self.published_details)
        self.title_label.bind('<Button-1>', self.open_headline)
        self.published_details_label.grid(row=0, column=0)
        self.title_label.grid(row=1, column=0)
        self.after(15000, self.show_headlines)

    # open headlines to view
    def open_headline(self, event):
        url = format(self.headline_url.get())
        kbg.webbrowser.open_new_tab(url)
