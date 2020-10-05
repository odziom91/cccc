import json
import requests


def GetDiscogsData(nr_release):
    songs = []
    artists = []
    title = []
    if nr_release != "":
        r = requests.get("https://api.discogs.com/releases/" + nr_release)
        json_string = json.loads(r.text)
        title = json_string["title"]
        for i, txt in enumerate(json_string["artists"]):
            artists.append(json_string["artists"][i]["name"])
        for i, txt in enumerate(json_string["tracklist"]):
            song = json_string["tracklist"][i]["title"]
            if json_string["tracklist"][i]["duration"] != "":
                duration = json_string["tracklist"][i]["duration"]
            else:
                duration = "0:00"
            songs.append(song + " [" + duration + "]")
    return (artists, title, songs)