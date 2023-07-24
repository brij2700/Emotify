from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, jsonify
import os
import sys
import spotipy
import spotipy.util as util
from spotipy import oauth2
import random
import time
from speech_main import mainrun
from moodify import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, create_playlist

client_id = "684b5c5b4e314dc3b5773577f96628b7"
client_secret = "ddfd6eec7f1e4a539168a9959f6c9c09"
redirect_uri = "http://localhost:8888/"
scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

access_token = ""
sp_oauth = None

app = Flask(__name__)


# render username page
@app.route('/')
def my_form():
    print("Done")
    return render_template('username.html')




# sends auth request
@app.route('/', methods=['POST'])
def index():
    print("Done2")
    username = request.form['username']
    cache = ".cache-" + username
    global sp_oauth
    global access_token
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, cache_path=cache)

    auth_url = sp_oauth.get_authorize_url()
    # get cached token
    token_info = sp_oauth.get_cached_token()

    # if cached token exists, get it
    if token_info:
        print("Found cached token!")
        milli_sec = int(round(time.time()))
        expiry = token_info['expires_at']

        # refresh token if expired
        if milli_sec >= int(expiry):
            print('token expired')
            return redirect(auth_url)
        # if token hasn't expired
        else:
            access_token = token_info['access_token']

            return render_template('selection.html')
    # if no cached token, get a new access token
    else:
        return redirect(auth_url)

print("Done")

@app.route('/video')
def indexload():
    return render_template('index.html')

@app.route('/audio')
def indexloadaudio():
    return render_template('index2.html')

@app.route('/audiosubmit')
def calculateEmo():
    #spotifyemo=mainrun()
    playlist = mainrun()
    print(playlist)

    return render_template('playlist.html',playlist=playlist)

# display playlist page
@app.route('/results')
def results():
    print ("in results")
    playlist = request.args.get('url',False)

    return render_template('playlist.html', playlist=playlist)

print("Done")

# get new access token
@app.route('/callback/')
def my_callback():
    global access_token
    global sp_oauth

    url = request.url
    # get access token from spotify
    code = sp_oauth.parse_response_code(url)
    if code:
        print("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

    if access_token:
        return render_template('index.html')

    else:
        return render_template('username.html')


# create plalist
@app.route("/moodify", methods=['POST'])
def moodify():
    global access_token
    mood = request.json['mood']
    mood_string = request.json['mood_string']

    mood = float(mood)

    spotify_auth = authenticate_spotify(access_token)
    top_artists = aggregate_top_artists(spotify_auth)
    top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
    selected_tracks = select_tracks(spotify_auth, top_tracks, mood)
    playlist = create_playlist(spotify_auth, selected_tracks, mood, mood_string)
    res = make_response(jsonify({
        "result": playlist
    }), 200)

    return res

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 8888))
    app.run(host="localhost",port=8888,debug=True)