import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
SELECTED_DATE = "2000-01-01"
load_dotenv()

response = requests.get(f"{URL}{SELECTED_DATE}/")
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
all_songs = []

all_songs_html = soup.select(selector="h3#title-of-a-story.c-title.a-no-trucate")


def format_text(str_val):
    str_val = str_val.replace("\n", "")
    str_val = str_val.replace("\t", "")
    return str_val


for tag in all_songs_html:
    song_name = format_text(tag.getText())
    all_songs.append(song_name)

print(all_songs)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print(client_id)
print(client_secret)
scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://example.com",
                              scope="playlist-modify-private", cache_path="token.txt"))
print(sp.current_user()["display_name"])
print(sp.current_user())
user_id = sp.current_user()["id"]
selected_year = SELECTED_DATE[0:4]
uris = []
for song in all_songs:
    result = sp.search(q=f"track:{song} year:{selected_year}", type="track")
    try:
        track_uri = result["tracks"]["items"][0]["uri"]
        uris.append(track_uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(uris)
playlist = sp.user_playlist_create(user=user_id, name=f"{SELECTED_DATE} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist["id"], uris)
