# HUGE shoutout to Simon Quick who's Spotify project was immensely helpful in using Flask to interact with the Spotify API
# Some of these functions are taken line for line from his project - if it had been a library I would just used import SimonsLibrary
import time
import requests
from flask import request
import json

def get_access_token(code, authorization):
    print ('Getting the access token')
    post_url = 'https://accounts.spotify.com/api/token'
    grant_type = 'authorization_code'
    # callback_url = 'http://127.0.0.1:5000/callback'
    callback_url = request.url_root + 'logged_in'
    #authorization = config.authorization

    post = {'redirect_uri': callback_url, 'code': code, 'grant_type': grant_type}
    headers = {'Authorization': authorization, 'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(post_url, headers=headers, data=post)
    auth_json = json.loads(r.text)
    try:
        access_token = 'Bearer ' + auth_json['access_token']
        print (access_token)
        return access_token
    except Exception as e:
        print ("Something went wrong at the Spotify end - press back and try again")
        return "Something went wrong at the Spotify end - press back and try again"


def create_playlist(access_token, user_id, title):
    cp_headers = {'Authorization': access_token, 'Content-Type': 'application/x-www-form-urlencoded'}
    cp_post = {'name': title, 'public': 'true', 'collaborative': 'false',
               'description': 'testing this out'}
    cp_url = 'https://api.spotify.com/v1/users/' + user_id.decode("utf-8") + '/playlists'
    r_cp = requests.post(cp_url, headers=cp_headers, data=json.dumps(cp_post))

    print (r_cp.status_code)

    if str(r_cp.status_code) != '201':
        print (r_cp.json())

        return "It didnt work yo - try again"
    r_cp_json = r_cp.json()
    playlist_id = r_cp_json['id']
    owner_id = r_cp_json['owner']['id']
    #full_pl = base64.b64encode(owner_id + '/' + playlist_id)
    # for delay testing purposes
    return playlist_id #full_pl

def get_all_playlists(access_token, user_id):
        api_headers = {'Authorization': access_token}
        # Set max number of playlists to be 50
        api_url = 'https://api.spotify.com/v1/me/playlists?limit=50'
        api_get_response = requests.get(api_url, headers = api_headers )
        all_playlists_json = api_get_response.json()
        return all_playlists_json

# Given sructured JSON of all playlists returned from spotify API, get an array of the names
def get_all_playlist_names(all_playlists_json):
    all_playlist_names = []
    for playlist in all_playlists_json['items']:
        all_playlist_names.append(playlist['name'])
        print(playlist['name'])
    return all_playlist_names

