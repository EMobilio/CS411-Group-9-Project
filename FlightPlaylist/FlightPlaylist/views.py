from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FlightSerializer
import requests



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

    return redirect('http://localhost:3000') #No URL yet

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
def get_data(request):
    if request.method == 'GET':
        #serializer = FlightSerializer(request.data)
        print(request.GET.get("flight_number"))
        return Response({"hello": "hello"})

@api_view(['GET'])
def get_flight_info(request):
    flight_code = request.GET.get("flight_number")
    access_key = settings.FLIGHT_ACCESS_KEY
    url = f"http://api.aviationstack.com/v1/flights"
    params = {
        'access_key': access_key,
        'flight_icao': flight_code
    }

    try:
        response = requests.get(url, params=params)
        print(response.text)

        if response.status_code == 200:
            data = response.json()
            if data['pagination']['total'] > 0:
                flight = data['data'][0]
                arrival = flight['arrival']
                return Response({
                    'flight': flight_code,
                    'destination': arrival['airport'],
                    'duration': arrival['estimated_runway']
                })
            else:
                return Response({"error": "Flight not found"})
        else:
            return Response({"error": "Failed to fetch data"})
    except Exception as e:
        return Response({"error": f"An exception occurred: {str(e)}"})


