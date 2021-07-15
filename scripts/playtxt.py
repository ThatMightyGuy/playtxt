# Version: 1.11
### Features ###
# * Added save states - use flag -C to continue where you left off
# * Added janky code

import re, requests, subprocess, urllib.parse, urllib.request, sys, os
from bs4 import BeautifulSoup

args = sys.argv
def playarray(playlist):
    for song_name in playlist:
        # Song and comment ignoring
        main.line += 1
        if song_name.isspace():
            print('Empty/whitespace string. Skipping')
            continue
        if song_name.startswith('##'):
            continue
        playsong(song_name)
def playsong(song_name):
    # Search for song and get song URL
    query_string = urllib.parse.urlencode({"search_query": song_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    inspect = BeautifulSoup(clip.content, "html.parser")
    yt_title = inspect.find_all("meta", property="og:title")
    for concatMusic1 in yt_title:
        pass
    # Play a song
    print('--- Now playing ---')
    print(song_name + 'from')
    print(clip2)
    print('YouTube video name is')
    print(concatMusic1['content'])
    try:
        main.songs += 1
        subprocess.Popen('mpv ' + clip2 + " --no-video --input-ipc-server=/tmp/mpvsocket > ~/.playtxt/mpv.log", shell=True).wait()
    except subprocess.CalledProcessError:
        print('Something really wrong happened with mpv')
        print('You probably should file a bug report on PlayTXT GitHub page')
        print('Attach the mpv output, which is saved at ~/.playtxt/mpv.log')
        exit()

def showhelp():
    print('PlayTXT - YouTube audio stream player...')
    print('...that can only play songs from a text file with song names')
    showusage()
    print('File structure is just a list of song names, each on its separate main.line')
    print('Pretty much entirely made from this StackOverflow question')
    print('https://stackoverflow.com/questions/49354232/how-to-stream-audio-from-a-youtube-url-in-python-without-download')

def showusage():
    print('Usage: playtxt.py -F (--file) <file> - plays a playlist')
    print('Usage: playtxt.py -N (--name) <song name> - plays a specific song')
    print('Usage: playtxt.py -C (--continue) - continue playing from a saved state')
    print('Usage: playtxt.py -h (--help) - displays this message')

def main():
    main.songs = 0
    mode = 0
    main.line = 0    
    try:
        playlist = []
        try:
            # Handle arguments
            if args[1] == '--help' or args[1] == '-h':
                showhelp()
            elif args[1] == '-F' or args[1] == '--file':
                path = args[2]
                playlist = open(path, 'r')
                mode = 1
            elif args[1] == '-N' or args[1] == '--name':
                song_name = ''
                # The next 3 lines are why I now love Python, lol
                for arg in args[2:]:
                    song_name += ' ' + arg
                path = song_name[1:]
                playlist = [path + '\n']
                mode = 2
            elif args[1] == '-C' or args[1] == '--continue':
                # god this is a huge mess
                try:
                    if os.stat(os.getenv('HOME') + '/.playtxt/playtxt-state').st_size == 0:
                        print('Save state is empty')
                        exit()
                    state = open(os.getenv('HOME') + '/.playtxt/playtxt-state', 'r').readlines()
                except FileNotFoundError:
                    print('Save state not found')
                    exit()
                mode = int(state[0])
                path = state[1]
                main.line = int(state[2])
                if mode == 1:
                    playlist = open(path.strip(), 'r').readlines()[main.line - 1:]
                    playarray(playlist)
                elif mode == 2:
                    playsong(path)
                else:
                    print('Corrupt save state')
                    print(state)
                    exit()
            else:
                print('Invalid usage')
                showusage()
                exit()
        except IndexError:
            print('Nothing to do, perhaps invalid usage?')
            showusage()
            exit()
        except FileNotFoundError:
            print('File does not exist')
            exit()
        playarray(playlist)
        print('Done, ' + str(main.songs) + ' songs played')
    except KeyboardInterrupt:
        print('\nInterrupted by user, ' + str(main.songs) + ' songs played')
        if input('Save state? (Y/n) ').lower().strip() != 'n':
            f = open(os.getenv('HOME') + '/.playtxt/playtxt-state', 'w')
            f.write(str(mode) + '\n' + path.strip() + '\n' + str(main.line - 1))
        else:
            exit()
if __name__ == "__main__":
    main()
