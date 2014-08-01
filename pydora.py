import os
from StringIO import StringIO
from ConfigParser import RawConfigParser
import pandora
import requests
import time
import random

CONFIG_PATH = '~/.config/pianobarfly/config'

conf_str = open(os.path.expanduser(CONFIG_PATH)).read()
conf_buf = StringIO('[pydora]\n' + conf_str)
conf = RawConfigParser()
conf.readfp(conf_buf)
auth_user = conf.get('pydora', 'user')
auth_pass = conf.get('pydora', 'password')
audio_dir = conf.get('pydora', 'audio_file_dir')

pan = pandora.Pandora()
pan.authenticate(auth_user, auth_pass)

for station in pan.stations:
    if station['isQuickMix']:
        pan.switch_station(station)

for _ in range(10):
    song = pan.get_next_song()
    artist = song['artistName'].replace('/', '-')
    songname = song['songName'].replace('/', '-')
    album = song['albumName'].replace('/', '-')
    rating = song['songRating']
    gain = song['trackGain']
    url = song['audioUrlMap']['highQuality']['audioUrl']
    path_fmt = "{}/{}/{}-{}".format(artist, album, artist, songname)
    path_fmt = path_fmt.replace(' ', '_')
    short_name = path_fmt + ".mp3"
    new_name = path_fmt + ".m4a"
    long_path = os.path.join(audio_dir, short_name)
    new_path = os.path.join(audio_dir, new_name)
    dirpath = os.path.dirname(long_path)
    print long_path, rating, gain
    try:
        if rating != 1:
            continue
        if not os.path.exists(long_path):
            if not os.path.exists(dirpath):
                # print "creating path", dirpath
                os.makedirs(dirpath)
            response = requests.get(url)
            response.raise_for_status()
            # print response.status_code, len(response.content)
            # print "writing file", long_path
            with open(long_path, 'wb') as fd:
                fd.write(response.content)
    except os.error:
        continue
    except requests.exceptions.RequestException:
        continue
    time.sleep(60 + random.randint(1, 60))
