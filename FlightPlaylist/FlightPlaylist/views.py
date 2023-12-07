from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta



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

    return redirect('') #No URL yet

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




