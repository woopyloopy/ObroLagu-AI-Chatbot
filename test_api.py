from music_api import search_song

songs = search_song("Coldplay")

for song in songs:
    print(song)