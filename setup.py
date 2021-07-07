from setuptools import setup
setup(
    name = 'playtxt',
    version = '1.0',
    description = 'YouTube audio stream player...that can only play songs from a text file with song names',
    author = 'JetFly',
    author_email = 'cakeislie.ilya@gmail.com',
    scripts = [
        'scripts/playtxt.py'
    ],
    data_files = [
        ('~/.playtxt', [])
    ]
)