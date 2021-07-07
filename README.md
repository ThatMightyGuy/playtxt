# playtxt
YouTube audio stream player...
...that can only play songs from a text file with song names

Pretty useful, if you ask me.

### Dependencies
[pip] bs4 requests
`pip install bs4 requests`

[pacman] youtube-dl mpv
`sudo pacman -S youtube-dl mpv`

### Installation
`sudo python setup.py install`

Usage: `playtxt.py <file>`

For help, ~~scream~~ `playtxt.py -h` or `playtxt.py --help`

It was cobbled together in an hour, from a StackOverflow question somebody asked.

TODO:

Play/pause/skip commands

Volume control

Save/resume exit states

Looping
