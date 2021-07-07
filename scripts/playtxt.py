import re, requests, subprocess, urllib.parse, urllib.request, sys
from bs4 import BeautifulSoup

args = sys.argv
try:
    if args[1] == '--help' or args[1] == '-h':
        print('PlayTXT - YouTube audio stream player...')
        print('...that can only play songs from a text file with song names')
        print('Usage: playtxt.py <file>')
        print('-h or --help displays this message')
        print('File structure is just a list of song names, each on its separate line')
        print('Pretty much entirely made from this StackOverflow question')
        print('https://stackoverflow.com/questions/49354232/how-to-stream-audio-from-a-youtube-url-in-python-without-download')
    playlist = open(args[1])
except IndexError:
    print('Usage: playtxt <file>')
    exit()
except FileNotFoundError:
    print('File does not exist')
    exit()
for song_name in playlist:
    query_string = urllib.parse.urlencode({"search_query": song_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print('--- Now playing ---')
    print(song_name + 'from')
    print(clip2)
    inspect = BeautifulSoup(clip.content, "html.parser")
    yt_title = inspect.find_all("meta", property="og:title")
    for concatMusic1 in yt_title:
        pass
    print('YouTube video name is')
    print(concatMusic1['content'])
    try:
        subprocess.Popen('mpv ' + clip2 + " --no-video --input-ipc-server=/tmp/mpvsocket > ~/.playtxt/mpvoutput.txt", shell=True).wait()
    except subprocess.CalledProcessError:
        print('This program requires: mpv youtube-dl [pip] bs4 [pip] requests')
        print('If dependencies are met, something really wrong happened with mpv')
        exit()
