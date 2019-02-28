


# Want an object that encapsulates our API pull of tracks and subsequent API pull of recommendations and features
# Playlist_Base Class
# Has:
# MUST BE SPECIFIED AT CREATE TIME
# username - spotify username
# toke - auth toeken from user logging in
# CAN BE SPECIFIED LATER
# playlist_name

# From that generate:
# orig_playlist_dict
# orig_playlist_df
# playlist_rec_something? (am I storing this as a list or dict)
# playlist_rec_df



# Functions and Organization is important
# Will want some of these functions when initializing a Playlist_Base

import spotipy
from time import time
from pearing_core_functions import get_tracks_from_playlist, get_track_features, get_similar_tracks_from_playlist

class Playlist_Base():
    def __init__(self, playlist_name = '', user_id = '', access_token = ''):
        
        cur_time = time()

        self.playlist_name = playlist_name
        self.user_id = user_id
        self.access_token = access_token
        # Access_token from spotify_api has 'Bearer ' in front
        # Spotipy token built on not having Bearer, so ditch that
        self.sp_token = access_token[7:]
        try:
            sp = spotipy.Spotify(auth=self.sp_token)
            #all_api_playlists = sp.user_playlists(self.user_id)
            self.spotipy_connection = sp
        except:
            print("Something went wrong hitting spotify API - did you provide the right token and username?")
        #sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(self.user_id)
        


        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('Initalized first set: ', elapsed_time)

        self.generate_from_playlist_name(playlist_name)


        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('finished generate_from_playlist_name: ', elapsed_time)
        
        # takes a playlist_name and populates all other relevant variables of object
    # If a new playlist name is passed, it will overwrite all values
    def generate_from_playlist_name(self, playlist_name):
        cur_time = time()

        self.playlist_name = playlist_name
        # Get all user's playlists from API PSI: Maybe there's a function that lets you hit API with playlist_name?
        sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(self.user_id)
        
        for api_playlist in all_api_playlists['items']:
            if(api_playlist['name'] == playlist_name):
                self.orig_playlist_dict = api_playlist
        

        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('ran over all playlists: ', elapsed_time)
        
        # Now have the original playlist
        
        #TODO: Get features of this playlist, then build rec playlist then get features of that
        
        ### GET FEATURES OF ORIGINAL PLAYLIST
        
        orig_playlist_tracks_tmp = get_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)

        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('got tracks from playlist: ', elapsed_time)
        

        self.orig_playlist_tracks_df = get_track_features(orig_playlist_tracks_tmp, self.access_token, self.user_id)
        
        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('Got features of original playlist: ', elapsed_time)
        

        #self.track_features = get_track_features(track_df, playlist_name):
        ### CREATE RECS FROM PLAYLIST -- PFI: could make this function much more robust, look at artist/genre too
        # Get recommended tracks as dict
        rec_tracks_tmp = get_similar_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)
        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('got rec tracks: ', elapsed_time)
        

        self.rec_tracks_df = get_track_features(rec_tracks_tmp, self.access_token, self.user_id)
        
        prev_time = cur_time
        cur_time = time() 
        elapsed_time = cur_time - prev_time

        print('Got rec track features ', elapsed_time)
        
        ### GET FEATURES OF REC PLAYLIST -- PSI: make get_features function faster
        
        
        
    def print_playlist_name(self):
        print(self.playlist_name)


# In[ ]:




