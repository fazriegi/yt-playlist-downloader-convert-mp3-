from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp
import re
import sys


if len(sys.argv) != 3:
    print(f'(+) Usage: {sys.argv[0]} <url> <output>.')
    print(f'(+) Example: {sys.argv[0]} https://youtube.com/ /home/user/')
    
path = sys.argv[2]
url = sys.argv[1]

playlist = Playlist(url)

#prints address of each YouTube object in the playlist
for vid in playlist.videos:
    print(vid)
    
for url in playlist:
    YouTube(url).streams.first().download(path)

for file in os.listdir(path):
    if re.search('mp4', file):
        mp4_path = os.path.join(path,file)
        mp3_path = os.path.join(path,os.path.splitext(file)[0]+'.mp3')
        new_file = mp.AudioFileClip(mp4_path)
        new_file.write_audiofile(mp3_path)
        os.remove(mp4_path)
