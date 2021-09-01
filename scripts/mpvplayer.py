import re, requests, urllib.parse, urllib.request, subprocess, platform, os
from bs4 import BeautifulSoup
import playtxt

# This file handles mpv playback, but cannot control it

def playarray(playlist):
    songs = 0
    for song_name in playlist:
        # Song and comment ignoring
        playtxt.line += 1
        playtxt.path = song_name
        if song_name.isspace():
            print('Empty/whitespace string. Skipping')
            continue
        if song_name.startswith('##'):
            continue
        songs += 1
        exitcode = playsong(song_name)
        if exitcode == 0:
            break
    return songs

def playsong(song_name):
    try:
        # Search for song and get song URL
        query_string = urllib.parse.urlencode({"search_query": song_name})
        format_url = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", format_url.read().decode())
        clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
        clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
        inspect = BeautifulSoup(clip.content, "html.parser")
        yt_title = inspect.find_all("meta", property="og:title")
        concat_music1 = yt_title[-1]
        # Play a song
        print('--- Now playing ---')
        print(song_name + 'from')
        print(clip2)
        print('YouTube video name is')
        print(concat_music1['content'])
        if platform.system() == "Windows":
            subprocess.Popen('mpv ' + clip2 + f" --no-video --input-ipc-server={os.getenv('TEMP')}/mpvsocket > {os.getenv('APPDATA')}/ThatMightyGuy/PlayTXT/mpv.log", shell=True).wait()
        else:
            subprocess.Popen('mpv ' + clip2 + " --no-video --input-ipc-server=/tmp/mpvsocket > ~/.playtxt/mpv.log", shell=True).wait()
    except KeyboardInterrupt:
        return 0
    return 1