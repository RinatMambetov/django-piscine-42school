import requests
import json


def collect_imdb_data():
    API_KEY = "4279563e"
    URL = f"http://www.omdbapi.com/?apikey={API_KEY}"
    FILMS = ["tt8362852", "tt0065163", "tt0120616", "tt0034398", "tt3120314", "tt0367677", "tt1594913", "tt5884052",
             "tt1572315", "tt0329101", "tt0117342", "tt0810743", "tt0105643", "tt0024216", "tt0107290"]
    data = {}
    for film in FILMS:
        try:
            res = requests.get(URL, params={"i": film})
            if not res.ok:
                continue
        except requests.HTTPError as e:
            print(e)
            continue
        try:
            data[film] = json.loads(res.text)
            data[film]['rawRating'] = data[film]["imdbRating"]
            data[film]["imdbRating"] = round(float(data[film]["imdbRating"]))
        except json.decoder.JSONDecodeError as e:
            print(e)
            continue
    return data
