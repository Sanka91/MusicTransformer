import collections
import os
import shutil
import pandas as pd

playlist_path = "C:\\Users\Phili\Desktop\Playlist_converter\\"
song_output = "C:\\Users\Phili\Desktop\All songs of playlists\\"

counter = 0
for root, dir, files in os.walk(playlist_path):
    for file in files:
        with open(os.path.join(root, file), "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip("\n")
                local_pc_path = line
                file_name = local_pc_path.split("\\")[-1]
                print(local_pc_path)
                print(song_output+file_name)
                a = shutil.copy2(local_pc_path, os.path.join(song_output, file_name))
                counter += 1

print(counter)



