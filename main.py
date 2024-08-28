import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id='Your Id',
        client_secret='Your Secret',
        redirect_uri='https://example.com/',
        show_dialog=True,
        cache_path='token.txt',
        username='Your Username'))

user_id = sp.current_user()['id']

input_ano_musicas = input('Qual ano você gostaria de pular? Escreva no formato YYYY-MM-DD: ')

site = f'https://www.billboard.com/charts/hot-100/{input_ano_musicas}/'

response = requests.get(site)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

titulo = soup.select('li ul li h3')
songs = [song.getText().strip() for song in titulo]

song_uris = []
year = input_ano_musicas.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"Playlist formada por integração", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)