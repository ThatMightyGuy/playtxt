# Help messages in a different file to clean up the code

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