# All actual songs need to be in /Internal storage/Music/ so that new playlists will find them on phone
import os

source_path = "C:\\Users\Phili\Desktop\Playlist_converter"
android_playlist_path = "/Internal storage/Music/"

for root, dirs, files in os.walk(source_path):
    for file in files:
        old_path = os.path.join(root, file)
        new_path = os.path.join(root,"New_"+ file)

        with open(old_path, "r+") as f, open(new_path, "w+") as n:
            for line in f:
                a = android_playlist_path + line.split("\\")[-1]
                n.write(a)
        # #
        remove = os.remove(old_path)
        rename = os.rename(new_path, old_path)

