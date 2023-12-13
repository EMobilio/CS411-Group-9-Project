import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from decouple import config
from countrycodes import country_dict
import os


#inputs: user_country: the name of the country they are traveling to
#       sp: spotipy instance
#       username: the user's username
#       token: the oauth token
#outputs: spotify playlist directly into the user's spotify library
def get_playlist_by_country_and_length(user_country,token): #generates playlist from top 200 songs
    sp = spotipyInit() #initialize spotipy
    user_profile = sp.me()  #get user profile
    
    country_code = country_dict[user_country]
    tracks = get_top_songs(token,country_code) #get top 200 songs
    #df = pd.DataFrame(tracks) #test to print out the top 200 songs returned from scrape
    #print(df.to_string(index=False))

    # Create a new playlist
    playlist_name = f"Top Songs from {user_country}"
    playlist_description = f"Top tracks from {user_country} for the flight"
    playlist = sp.user_playlist_create(user_profile['id'], playlist_name,public=False, description = playlist_description)
    playlist_id = playlist['id']

    # Add tracks to the playlist
    for entry in tracks:
        sp.playlist_add_items(playlist_id=playlist_id, items=[entry['uri']])

    #playlist was made and loaded
    print(f"Playlist '{playlist_name}' created with ID: {playlist_id}")
    print(f'https://open.spotify.com/playlist/{playlist_id}')
    return f'https://open.spotify.com/playlist/{playlist_id}'

def get_top_songs(token, country_code): #scrapes spotify regional chart and returns top 200 songs
    url = f'https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-{country_code}-weekly/2023-12-07'
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)

    chart = []
    for entry in response.json()['entries']:
        chart.append({
        "Rank": entry['chartEntryData']['currentRank'],
        "Artist": ', '.join([artist['name'] for artist in entry['trackMetadata']['artists']]),
        "TrackName": entry['trackMetadata']['trackName'],
        "uri": entry['trackMetadata']['trackUri']
        })
    return chart

def spotipyInit(): #EDIT ONCE WE CONNECT TO FRONTEND
    # Set your Spotify API credentials ()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    id = config('CLIENT_ID') #client id
    secret = config('CLIENT_SECRET') #client secret
    uri = config('REDIRECT_URI') #set to flight buddy website
    # Set up Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id,
                                                client_secret=secret,
                                                redirect_uri=uri,
                                                scope='playlist-modify-private'))
    return sp
