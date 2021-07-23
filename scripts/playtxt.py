#!/usr/bin/python
# Version: 1.11
### Features ###
# * Huge cleanup of the code was done.
# * Removed half of the janky code

import re, requests, subprocess, urllib.parse, urllib.request, sys, os
from bs4 import BeautifulSoup
import helpmsg, mpvplayer

args = sys.argv

global playtxt_path, songs, mode, line, path, playlist
playtxt_path = os.getenv('HOME') + '/.playtxt/playtxt-state'
songs = 0
mode = 0
line = 0
path = ""
playlist = []
def argument_continue():
    global playlist
    # god this is a huge mess
    try:
        if os.stat(playtxt_path).st_size == 0:
            print('Save state is empty')
            exit()
        state = open(playtxt_path, 'r').readlines()
        mode = int(state[0])
        path = state[1]
        line = int(state[2])
        if mode == 1:
            playlist = open(path.strip(), 'r').readlines()[line:]
        elif mode == 2:
            playlist = [path]
        else:
            print('Corrupt save state')
            print(state)
            exit()
    except FileNotFoundError:
        print('Save state not found')
        exit()

def argument_handler():
    global mode, path, playlist
    if args[1] == '--help' or args[1] == '-h': # Help
        helpmsg.showhelp()
    elif args[1] == '-F' or args[1] == '--file': # File player
        path = args[2]
        mode = 1
        playlist = open(path, 'r')
    elif args[1] == '-N' or args[1] == '--name': # Single song player
        song_name = ''
        for arg in args[2:]:
            song_name += ' ' + arg
        path = song_name[1:]
        mode = 2
        playlist = [path + '\n']
    elif args[1] == '-C' or args[1] == '--continue': # Continue
        argument_continue()
    else:
        print('Invalid usage')
        helpmsg.showusage()
        exit()

def save():
    print('\nInterrupted by user, ' + str(songs) + ' songs played')
    if input('Save state? (Y/n) ').lower().strip() != 'n':
        open(playtxt_path, 'w').write(str(mode) + '\n' + path.strip() + '\n' + str(line))
    else:
        exit()

def main():
    global playlist
    try:
        argument_handler()
        songs = mpvplayer.playarray(playlist)
        print('Done, ' + str(songs) + ' songs played')
        save()
    except IndexError:
        print('Nothing to do, perhaps invalid usage?')
        helpmsg.showusage()
        exit()
    except FileNotFoundError:
        print('File does not exist')
        exit()

if __name__ == "__main__":
    main()
