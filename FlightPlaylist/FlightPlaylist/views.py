from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pandas as pd
from decouple import config

country_dict = {'Afghanistan': 'AF',
 'Albania': 'AL',
 'Algeria': 'DZ',
 'American Samoa': 'AS',
 'Andorra': 'AD',
 'Angola': 'AO',
 'Anguilla': 'AI',
 'Antarctica': 'AQ',
 'Antigua and Barbuda': 'AG',
 'Argentina': 'AR',
 'Armenia': 'AM',
 'Aruba': 'AW',
 'Australia': 'AU',
 'Austria': 'AT',
 'Azerbaijan': 'AZ',
 'Bahamas': 'BS',
 'Bahrain': 'BH',
 'Bangladesh': 'BD',
 'Barbados': 'BB',
 'Belarus': 'BY',
 'Belgium': 'BE',
 'Belize': 'BZ',
 'Benin': 'BJ',
 'Bermuda': 'BM',
 'Bhutan': 'BT',
 'Bolivia, Plurinational State of': 'BO',
 'Bonaire, Sint Eustatius and Saba': 'BQ',
 'Bosnia and Herzegovina': 'BA',
 'Botswana': 'BW',
 'Bouvet Island': 'BV',
 'Brazil': 'BR',
 'British Indian Ocean Territory': 'IO',
 'Brunei Darussalam': 'BN',
 'Bulgaria': 'BG',
 'Burkina Faso': 'BF',
 'Burundi': 'BI',
 'Cambodia': 'KH',
 'Cameroon': 'CM',
 'Canada': 'CA',
 'Cape Verde': 'CV',
 'Cayman Islands': 'KY',
 'Central African Republic': 'CF',
 'Chad': 'TD',
 'Chile': 'CL',
 'China': 'CN',
 'Christmas Island': 'CX',
 'Cocos (Keeling) Islands': 'CC',
 'Colombia': 'CO',
 'Comoros': 'KM',
 'Congo': 'CG',
 'Congo, the Democratic Republic of the': 'CD',
 'Cook Islands': 'CK',
 'Costa Rica': 'CR',
 'Croatia': 'HR',
 'Cuba': 'CU',
 'Curaçao': 'CW',
 'Cyprus': 'CY',
 'Czech Republic': 'CZ',
 "Côte d'Ivoire": 'CI',
 'Denmark': 'DK',
 'Djibouti': 'DJ',
 'Dominica': 'DM',
 'Dominican Republic': 'DO',
 'Ecuador': 'EC',
 'Egypt': 'EG',
 'El Salvador': 'SV',
 'Equatorial Guinea': 'GQ',
 'Eritrea': 'ER',
 'Estonia': 'EE',
 'Ethiopia': 'ET',
 'Falkland Islands (Malvinas)': 'FK',
 'Faroe Islands': 'FO',
 'Fiji': 'FJ',
 'Finland': 'FI',
 'France': 'FR',
 'French Guiana': 'GF',
 'French Polynesia': 'PF',
 'French Southern Territories': 'TF',
 'Gabon': 'GA',
 'Gambia': 'GM',
 'Georgia': 'GE',
 'Germany': 'DE',
 'Ghana': 'GH',
 'Gibraltar': 'GI',
 'Greece': 'GR',
 'Greenland': 'GL',
 'Grenada': 'GD',
 'Guadeloupe': 'GP',
 'Guam': 'GU',
 'Guatemala': 'GT',
 'Guernsey': 'GG',
 'Guinea': 'GN',
 'Guinea-Bissau': 'GW',
 'Guyana': 'GY',
 'Haiti': 'HT',
 'Heard Island and McDonald Islands': 'HM',
 'Holy See (Vatican City State)': 'VA',
 'Honduras': 'HN',
 'Hong Kong': 'HK',
 'Hungary': 'HU',
 'Iceland': 'IS',
 'India': 'IN',
 'Indonesia': 'ID',
 'Iran, Islamic Republic of': 'IR',
 'Iraq': 'IQ',
 'Ireland': 'IE',
 'Isle of Man': 'IM',
 'Israel': 'IL',
 'Italy': 'IT',
 'Jamaica': 'JM',
 'Japan': 'JP',
 'Jersey': 'JE',
 'Jordan': 'JO',
 'Kazakhstan': 'KZ',
 'Kenya': 'KE',
 'Kiribati': 'KI',
 "Korea, Democratic People's Republic of": 'KP',
 'Korea, Republic of': 'KR',
 'Kuwait': 'KW',
 'Kyrgyzstan': 'KG',
 "Lao People's Democratic Republic": 'LA',
 'Latvia': 'LV',
 'Lebanon': 'LB',
 'Lesotho': 'LS',
 'Liberia': 'LR',
 'Libya': 'LY',
 'Liechtenstein': 'LI',
 'Lithuania': 'LT',
 'Luxembourg': 'LU',
 'Macao': 'MO',
 'Macedonia, the former Yugoslav Republic of': 'MK',
 'Madagascar': 'MG',
 'Malawi': 'MW',
 'Malaysia': 'MY',
 'Maldives': 'MV',
 'Mali': 'ML',
 'Malta': 'MT',
 'Marshall Islands': 'MH',
 'Martinique': 'MQ',
 'Mauritania': 'MR',
 'Mauritius': 'MU',
 'Mayotte': 'YT',
 'Mexico': 'MX',
 'Micronesia, Federated States of': 'FM',
 'Moldova, Republic of': 'MD',
 'Monaco': 'MC',
 'Mongolia': 'MN',
 'Montenegro': 'ME',
 'Montserrat': 'MS',
 'Morocco': 'MA',
 'Mozambique': 'MZ',
 'Myanmar': 'MM',
 'Namibia': 'NA',
 'Nauru': 'NR',
 'Nepal': 'NP',
 'Netherlands': 'NL',
 'New Caledonia': 'NC',
 'New Zealand': 'NZ',
 'Nicaragua': 'NI',
 'Niger': 'NE',
 'Nigeria': 'NG',
 'Niue': 'NU',
 'Norfolk Island': 'NF',
 'Northern Mariana Islands': 'MP',
 'Norway': 'NO',
 'Oman': 'OM',
 'Pakistan': 'PK',
 'Palau': 'PW',
 'Palestine, State of': 'PS',
 'Panama': 'PA',
 'Papua New Guinea': 'PG',
 'Paraguay': 'PY',
 'Peru': 'PE',
 'Philippines': 'PH',
 'Pitcairn': 'PN',
 'Poland': 'PL',
 'Portugal': 'PT',
 'Puerto Rico': 'PR',
 'Qatar': 'QA',
 'Romania': 'RO',
 'Russian Federation': 'RU',
 'Rwanda': 'RW',
 'Réunion': 'RE',
 'Saint Barthélemy': 'BL',
 'Saint Helena, Ascension and Tristan da Cunha': 'SH',
 'Saint Kitts and Nevis': 'KN',
 'Saint Lucia': 'LC',
 'Saint Martin (French part)': 'MF',
 'Saint Pierre and Miquelon': 'PM',
 'Saint Vincent and the Grenadines': 'VC',
 'Samoa': 'WS',
 'San Marino': 'SM',
 'Sao Tome and Principe': 'ST',
 'Saudi Arabia': 'SA',
 'Senegal': 'SN',
 'Serbia': 'RS',
 'Seychelles': 'SC',
 'Sierra Leone': 'SL',
 'Singapore': 'SG',
 'Sint Maarten (Dutch part)': 'SX',
 'Slovakia': 'SK',
 'Slovenia': 'SI',
 'Solomon Islands': 'SB',
 'Somalia': 'SO',
 'South Africa': 'ZA',
 'South Georgia and the South Sandwich Islands': 'GS',
 'South Sudan': 'SS',
 'Spain': 'ES',
 'Sri Lanka': 'LK',
 'Sudan': 'SD',
 'Suriname': 'SR',
 'Svalbard and Jan Mayen': 'SJ',
 'Swaziland': 'SZ',
 'Sweden': 'SE',
 'Switzerland': 'CH',
 'Syrian Arab Republic': 'SY',
 'Taiwan, Province of China': 'TW',
 'Tajikistan': 'TJ',
 'Tanzania, United Republic of': 'TZ',
 'Thailand': 'TH',
 'Timor-Leste': 'TL',
 'Togo': 'TG',
 'Tokelau': 'TK',
 'Tonga': 'TO',
 'Trinidad and Tobago': 'TT',
 'Tunisia': 'TN',
 'Turkey': 'TR',
 'Turkmenistan': 'TM',
 'Turks and Caicos Islands': 'TC',
 'Tuvalu': 'TV',
 'Uganda': 'UG',
 'Ukraine': 'UA',
 'United Arab Emirates': 'AE',
 'United Kingdom': 'GB',
 'United States': 'US',
 'United States Minor Outlying Islands': 'UM',
 'Uruguay': 'UY',
 'Uzbekistan': 'UZ',
 'Vanuatu': 'VU',
 'Venezuela, Bolivarian Republic of': 'VE',
 'Viet Nam': 'VN',
 'Virgin Islands, British': 'VG',
 'Virgin Islands, U.S.': 'VI',
 'Wallis and Futuna': 'WF',
 'Western Sahara': 'EH',
 'Yemen': 'YE',
 'Zambia': 'ZM',
 'Zimbabwe': 'ZW',
 'Åland Islands': 'AX'}

@login_required
def spotify_auth(request):
    sp_oauth = SpotifyOAuth(
        settings.SPOTIPY_CLIENT_ID,
        settings.SPOTIPY_CLIENT_SECRET,
        settings.SPOTIPY_REDIRECT_URI,
        scope='user-library-read playlist-modify-public',
    )

    token_info = sp_oauth.get_access_token(request.GET.get('code'))

    request.session['spotify_token_info'] = token_info

    return redirect('http://localhost:3000/') 

def handle_token_refresh(request, token_info):
    exp_time = datetime.fromtimestamp(token_info['expires_at'])
    if exp_time <= datetime.now() + timedelta(minutes=5):
        sp_oauth = SpotifyOAuth(
            settings.SPOTIPY_CLIENT_ID,
            settings.SPOTIPY_CLIENT_SECRET,
            settings.SPOTIPY_REDIRECT_URI,
            scope='user-library-read playlist-modify-public',            
        )
        new_token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        request.session['spotify_token_info'] = new_token_info

@api_view(['GET'])
def get_flight_info(request):
    airline_code = request.GET.get("flight_number")[0:2]
    flight_number = request.GET.get("flight_number")[2:]
    current_date = datetime.now()
    date = str(current_date.day + 1)
    month = str(current_date.month)
    year = str(current_date.year)
    soup = get_flight_details(airline_code, flight_number, date, month, year)
    airport  = get_airport_names(soup)
    country = get_country_code(airport)

    return Response({"country": country})
    
def get_flight_details(airline_code, flight_number, date, month, year):
    def get_data(url):
        response = requests.get(url)
        return response.text

    url = f"https://www.flightstats.com/v2/flight-tracker/{airline_code}/{flight_number}?year={year}&month={month}&date={date}"

    html_data = get_data(url)

    soup = BeautifulSoup(html_data, 'html.parser')

    return soup

def get_airport_names(soup):
    airport_names = [
        i.get_text()
        for i in soup.find_all(
            "div", class_="text-helper__TextHelper-sc-8bko4a-0"
        )
    ]
    return airport_names[4]

def get_country_code(airport):
    url = "https://forteweb-airportguide-airport-basic-info-v1.p.rapidapi.com/get_airport_by_iata"

    querystring = {"airport_id": airport, "auth":"authairport567"}

    headers = {
	    "X-RapidAPI-Key": settings.AIRPORT_KEY,
	    "X-RapidAPI-Host": settings.AIRPORT_HOST,
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['airport'][0]['country']
    
@api_view(['POST'])
def create_playlist(request):
    token = request.GET.get("token")
    user_country = request.GET.get("country_code")
    get_playlist_by_country_and_length(user_country, token)
    return Response({"message": "success"})

# Set your Spotify API credentials ()
CLIENT_ID = config('SPOTIFY_CLIENT_ID')#client id
CLIENT_SECRET = config('SPOTIFY_SECRET') #client secret
REDIRECT_URI = 'http://localhost:8000/accounts/login/spotify/callback' #set to flight buddy website

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

def spotipyInit(): 
    # Set up Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope='playlist-modify-private'))
    return sp