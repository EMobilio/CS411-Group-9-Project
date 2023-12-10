import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd

# Set your Spotify API credentials ()
CLIENT_ID =  #client id
CLIENT_SECRET =  #client secret
REDIRECT_URI =  #set to flight buddy website
USERNAME = #client username

#inputs: user_country: the ISO code the of the country they are traveling to
#       flight_duration: duration of the flight
#       sp: spotipy instance
#       username: the user's username
#       token: the oauth token
#outputs: spotify playlist directly into the user's spotify library
def get_playlist_by_country_and_length(user_country, flight_duration,token): #generates playlist from top 200 songs
    sp = spotipyInit() #initialize spotipy
    user_profile = sp.me()  #get user profile

    tracks = get_top_songs(token,user_country) #get top 200 songs
    #df = pd.DataFrame(tracks) #test to print out the top 200 songs returned from scrape
    #print(df.to_string(index=False))

    # Create a new playlist
    playlist_name = f"Top Songs from {user_country}"
    playlist_description = f"Top tracks from {user_country} for the flight"
    playlist = sp.user_playlist_create(user_profile['id'], playlist_name,public=False, description = playlist_description)
    playlist_id = playlist['id']

    #how many songs should be in the playlist (over estimate)
    num_songs = int(flight_duration/2)

    song_counter=0
    # Add tracks to the playlist
    for entry in tracks:
        sp.playlist_add_items(playlist_id=playlist_id, items=[entry['uri']])
        song_counter+=1
        if(song_counter>num_songs):
            break

    #playlist was made and loaded
    print(f"Playlist '{playlist_name}' created with ID: {playlist_id}")

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
    # Set up Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                username = USERNAME,
                                                scope='playlist-modify-private'))
    return sp