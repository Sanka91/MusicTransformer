# Playlist needs to be public
# Code only sees first 100 songs of playlist
# Most errors will come from "pattern" list in pytube's Cipher.py file --- Update that

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from pytube import YouTube
import os

# General variables
source_path = "C:\\Users\Phili\Desktop\Youtube_Songs"
file_path = "C:\\Users\Phili\Desktop\Youtube_Songs\Error_list.txt"

# Pytube variables
source = "https://www.youtube.com"

# Beautiful Soup variables
playlist_url = urlopen("https://www.youtube.com/playlist?list=PL6Kpk92an0p0l_Nv_n8dcGE2ebwhmxfZg&disable_polymer=true")
page_html = playlist_url.read()
page_soup = bs(page_html, "html.parser")
song_info = page_soup.findAll("td", {"class": "pl-video-title"})

def downloader_playlist():
    with open(file_path, "w") as ef:
        for index, name in enumerate(song_info):
            song_title = song_info[index].a.text
            song_url = song_info[index].a["href"]
            print("Downloading", song_title)
            try:
                yt_url = YouTube("{}{}".format(source, song_url))
                stream_choice = yt_url.streams.get_by_itag(140)
                stream_choice.download(source_path)

            except Exception as e:
                print(e)
                print(song_title + " had an error")
                ef.write(song_title)
                continue

downloader_playlist()
