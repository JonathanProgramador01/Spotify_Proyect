import pprint

import requests
import spotipy
import os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Este metodo es para cargar mis variables de mi archivo .env
load_dotenv()

date = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
solicitud = requests.get(url=URL)
soup = BeautifulSoup(solicitud.content, 'html.parser')

informacion = soup.select(selector="li h3")
songs = [informacion[i].get_text().strip() for i in range(len(informacion)) if i < 100]


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    redirect_uri=os.environ.get("URL"),
    show_dialog=True,
    cache_path="token.txt",
    scope="playlist-modify-private"))


USER_ID = sp.current_user()["id"]

url_song = []
year = date.split("-")[0]
for cancion in songs:
    try:
        result = sp.search(q=f"track:{cancion} year:{year}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        url_song.append(uri)
    except:
        print(f"Como esa cancion no existio {cancion}")

ID_PLAYLIST = sp.user_playlist_create(user=USER_ID, name=f"{year} Billboard 100", public=False)
ID_PLAYLIST = ID_PLAYLIST["id"]
sp.playlist_add_items(playlist_id=ID_PLAYLIST, items=url_song)

