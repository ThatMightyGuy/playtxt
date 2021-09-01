import platform, os
def check_data_dirs():
    if platform.system() == "Windows":
        if not os.path.exists(os.getenv('APPDATA') + "/ThatMightyGuy/PlayTXT"):
            os.makedirs(os.getenv('APPDATA') + "/ThatMightyGuy/PlayTXT")
    else:
        if not os.path.exists(os.getenv('HOME') + "/.playtxt"):
           os.makedirs(os.getenv('HOME') + "/.playtxt")