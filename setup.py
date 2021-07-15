from setuptools import setup
setup(
    name = 'playtxt',
    version = '1.2',
    description = 'YouTube audio stream player...that can only play songs from a text file with song names',
    author = 'Ilya (ThatMightyGuy, JetFly) Vitsev',
    author_email = 'cakeislie.ilya@gmail.com',
    scripts = [
        'scripts/playtxt.py'
    ],
    install_requires = [
        'bs4',
        'requests'
    ],
    data_files = [
        ('~/.playtxt', [])
    ]
)