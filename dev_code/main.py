from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import requests
import json
import datetime
from datetime import datetime
import spotipy
import numpy
import pandas as pd 
from functions import get_access_token, create_playlist, get_all_playlists, get_all_playlist_names
from python_pearing.pearing_class_functions import Pear_Playlists


app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")




@app.route("/logged_in")
def logged_in():
    code = request.args.get('code')
    
    access_token = get_access_token(code, app.config['AUTHORIZATION'])
    
    
    me_headers = {'Authorization': access_token}
    me_post = {}
    me_url = 'https://api.spotify.com/v1/me'

    r_me = requests.get('https://api.spotify.com/v1/me', headers=me_headers)
    r_me_json = json.loads(r_me.text)
    
    # For some reason we can't do 2 identical post requests in teh get_access_token function
    # Just catch it down here, if anything goes wrong just push back to home page
    try: 
        user_id_byte = r_me_json['id'].encode('utf-8')
        user_id_str = r_me_json['id']
        
        all_playlists_json = get_all_playlists(access_token, user_id_byte)
        all_playlists_names = get_all_playlist_names(all_playlists_json)

        # Pass access_token and user_id to be used on next page
        
        return render_template('logged_in.html', all_playlists_names = all_playlists_names, access_token = access_token, user_id = user_id_str)
    except Exception as e:
        return render_template('home.html')

@app.route("/login")
def login():
    callback_url = request.url_root + 'logged_in'
    base_url = 'https://accounts.spotify.com/en/authorize?client_id=' + app.config['CLIENT_ID'] + '&response_type=code&redirect_uri=' + callback_url + '&scope=user-read-email%20playlist-read-private%20user-follow-read%20user-library-read%20user-top-read%20playlist-modify-private%20playlist-modify-public&state=34fFs29kd09'
    response = make_response(redirect(base_url, 302))
    return response

@app.route('/pearing', methods = ['GET', 'POST'])
def pearing():
    
    playlist_name_1 = request.form['playlist_name_1']
    playlist_name_2 = request.form['playlist_name_2']
    user_id = request.form['user_id']
    access_token = request.form['access_token']
    
    #import time
    Pear_Playlists(playlist_name_1, playlist_name_2, access_token, user_id)
    #time.sleep(5)
    return render_template('pearing.html', playlist_name_1 = playlist_name_1, playlist_name_2 = playlist_name_2, user_id = user_id, access_token = access_token)


if __name__ == "__main__":
    app.run(debug=True)


