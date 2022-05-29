# Only works if music files have metadata that includes title and contributing artist
import os
import mutagen as mut
from mutagen.id3 import APIC, ID3, TIT2, TPE1, TALB
from mutagen.mp3 import EasyMP3 as MP3

source_path = "C:\\Users\Phili\Desktop\Mp3 Converter"
tag_dict = {"Artist_key": "TPE1",
            "Title_key": "TIT2",
            "Album_key": "TALB"
            }
filetype = ".mp3"

# Replacement strings for songs as file-naming conventions in Windows do not allow for these characters
rep_dict = {"\\" : "",
            "/" : "",
            "*" : "",
            "?" : "",
            '"' : "",
            ":" : "",
            "<" : "",
            ">" : "",
            "|" : "",
            "´" : "'"
            }


def add_missing_metadata(path, track):
    #track is passed in as a list and list comprehension deletes whitespaces in front/after artist and title
    track = [x.strip(" ") for x in track]

    #Adds Youtube as mutagen album tag if there was no album description before
    entry_album = "Youtube"

    try:
        artist_suggestion = input("Is the artist {}?    y/n".format(track[0]))
        if artist_suggestion == "y":
            entry_artist = track[0]
        else:
            entry_artist = input("What's the artist??")
    except:
        entry_artist = input("What's the artist??")


    try:
        title_suggestion = input("Is the title {}?      y/n".format(track[1]))
        if title_suggestion == "y":
            entry_title = track[1]
        else:
            entry_title = input("What's the title??")
    except:
        entry_title = input("What's the title??")

    new_string_func(entry_artist, entry_title, entry_album, path)


def new_string_func(artist, title, album, path):
    # Runs through dictionary and checks if keys are in artist or title
    for char in rep_dict:
        if char in artist or char in title or char in album:
            # Replaces characters from dictionary with empty strings. Then it deletes empty strings in front and after artist and title
            artist = artist.replace(char, rep_dict[char]).strip()
            title = title.replace(char, rep_dict[char]).strip()
            album = album.replace(char, rep_dict[char]).strip()

    new_file_name = "{} - {}{}".format(artist, title, filetype)

    audio_file = MP3(path, ID3=ID3)
    audio_file.tags.add(TPE1(encoding=3, text= "{}".format(artist)))
    audio_file.tags.add(TIT2(encoding=3, text= "{}".format(title)))
    audio_file.tags.add(TALB(encoding=3, text= "{}".format(album)))
    audio_file.tags.add(APIC(encoding=3))
    audio_file.pprint()
    audio_file.save()

    return new_file_name


for root, dirs, files in os.walk(source_path):
    # Runs through all tracks in all subfolders
    for track in files:
        # Creates exact path of single files
        single_file_path_old = os.path.join(root, track)
        # Checks if file ends with specific filetype (e.g. mp3)
        if track.endswith(filetype):
            counter1 = 0
            while counter1 == 0:
                #Runs through files as long as they don't have proper mutagen tags inserted
                try:
                    # Get artist and title from mutagen Metadata
                    artist = str(mut.File(single_file_path_old)[tag_dict["Artist_key"]]).title()
                    title = str(mut.File(single_file_path_old)[tag_dict["Title_key"]]).capitalize()
                    album = str(mut.File(single_file_path_old)[tag_dict["Album_key"]]).capitalize()
                    if artist == None or artist == "" or artist == " " or title == None or title == "" or title == " " or album == None or album == "" or album == " ":
                        # checks if mutagen tags are empty
                        print("Metadata has empty string function running")
                        print("Song description is: {}".format(track))
                        new_file_name = add_missing_metadata(single_file_path_old, track[:-len(filetype)].split("-"))
                    else:
                        print("File has metadata for artist, title and album")
                        counter1 = 1
                        new_file_name = new_string_func(artist, title, album, single_file_path_old)

                #only runs when there is no mutagen tags
                except:
                    print("Error function running")
                    print("Song description is {}".format(track))
                    new_file_name = add_missing_metadata(single_file_path_old,track[:-len(filetype)].split("-"))


            source_path_track_list = os.listdir(source_path)
            # Lists all files in target directory


            if new_file_name not in source_path_track_list:
                # Checks if the new file is already in target directory
                os.rename(single_file_path_old, "{}\\{}".format(source_path,new_file_name))
            else:
                print("{}  already exists in Directory".format(new_file_name))

                counter = 0
                while counter == 0:
                    # Loop that asks what to do if duplicate files are found in target directory
                    choice = input("Do you want to remove the duplicate file? y/n")
                    if choice == "y":
                        os.remove(single_file_path_old)
                        print("File was removed")
                        counter = 1
                    elif choice == "n":
                        print("File will be kept")
                        counter = 1
                    else:
                        print("Unknown input, try again")

# Metadata (artist, title und album) auch an gross und kleinschreibung anpassen

