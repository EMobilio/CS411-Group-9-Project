from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

