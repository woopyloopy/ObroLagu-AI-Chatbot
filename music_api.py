import requests

def search_song(keyword, limit=5):
    url = "https://itunes.apple.com/search"

    params = {
        "term": keyword,
        "entity": "song",
        "limit": limit
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    songs = []

    for item in data.get("results", []):
        songs.append({
            "track": item.get("trackName"),
            "artist": item.get("artistName"),
            "album": item.get("collectionName")
        })

    return songs