# Version: 1.1
### Changes ###
# * Changed command line syntax
# * Cleaned up the code a bit. Perhaps, it actually became dirtier
#   I'm in a love-hate relationship with Python. I love how it works, how easy it is to
#   do something, but man, is it hard to understand what's going on here
### Features ###
# * Added an ability to request a single song (-N / --name)
# * You can now make comments in playlists by starting a line with "##"
# * Now we actually handle ^C and count played songs

import re, requests, subprocess, urllib.parse, urllib.request, sys
from bs4 import BeautifulSoup

def playsong(song_name):
    # Search for song and get song URL
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
        main.songs += 1
    except subprocess.CalledProcessError:
        print('This program requires: mpv youtube-dl [pip] bs4 [pip] requests')
        print('If dependencies are met, something really wrong happened with mpv')
        exit()

def showhelp():
    print('PlayTXT - YouTube audio stream player...')
    print('...that can only play songs from a text file with song names')
    print('Usage: playtxt -F <file>')
    print('Usage: playtxt -N <song name>')
    print('-h or --help displays this message')
    print('File structure is just a list of song names, each on its separate line')
    print('Pretty much entirely made from this StackOverflow question')
    print('https://stackoverflow.com/questions/49354232/how-to-stream-audio-from-a-youtube-url-in-python-without-download')

args = sys.argv
# Handle command arguments
def main():
    main.songs = 0
    try:
        try:
            # --help
            if args[1] == '--help' or args[1] == '-h':
                showhelp()
            if args[1] == '-F' or args[1] == '--file':
                playlist = open(args[2])
            if args[1] == '-N' or args[1] == '--name':
                song_name = ''
                # The next 3 lines are why I now love Python, lol
                for arg in args[2:]:
                    song_name += ' ' + arg
                playlist = [song_name[1:] + '\n']
        except IndexError:
            showhelp()
            exit()
        except FileNotFoundError:
            print('File does not exist')
            exit()
        for song_name in playlist:
            # Song ignoring
            if song_name.isspace():
                print('Empty/whitespace string. Skipping')
                continue
            if song_name.startswith('##'):
                continue
            playsong(song_name)
        print('Done, ' + str(main.songs) + ' songs played')
    except KeyboardInterrupt:
        print('\nInterrupted by user, ' + str(main.songs) + ' songs played')
if __name__ == "__main__":
    main()
