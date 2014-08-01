import os
from StringIO import StringIO
from ConfigParser import RawConfigParser
import pandora
import requests
import time
import random
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error as id3_error


def add_id3_tag(path, artist, album, title):
    mp3 = EasyID3()
    mp3['artist'] = artist
    mp3['album'] = album
    mp3['title'] = title
    mp3.save(path)


def add_id3_art(path, url):
    try:
        art = requests.get(url)
        art.raise_for_status()

        mp3 = MP3(path, ID3=ID3)
        art_tag = APIC()
        art_tag.encoding = 3
        art_tag.type = 3
        art_tag.desc = u"Album Cover"
        if url.endswith('png'):
            art_tag.mime = u"image/png"
        else:
            art_tag.mime = u"image/jpeg"
        art_tag.data = art.content
        mp3.tags.add(art_tag)
        mp3.save()
    except requests.exceptions.RequestException:
        return
    except id3_error:
        return

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
    artist = song['artistName']
    songname = song['songName']
    album = song['albumName']
    rating = song['songRating']
    gain = song['trackGain']
    url = song['audioUrlMap']['highQuality']['audioUrl']
    art_url = song['albumArtUrl']
    artist_fmt = song['artistName'].replace('/', '-').encode('utf8', errors='ignore')
    title = song['songName'].replace('/', '-').encode('utf8', errors='ignore')
    album_fmt = song['albumName'].replace('/', '-').encode('utf8', errors='ignore')
    path_fmt = "{}/{}/{}-{}".format(artist_fmt, album_fmt, artist_fmt, title)
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
            add_id3_tag(long_path, artist, album, songname)
            add_id3_art(long_path, art_url)
    except os.error:
        continue
    except requests.exceptions.RequestException:
        continue
    time.sleep(60 + random.randint(1, 60))
