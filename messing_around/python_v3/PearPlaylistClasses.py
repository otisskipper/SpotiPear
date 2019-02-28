#!/usr/bin/env python
# coding: utf-8

# In[42]:


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


# In[52]:


# Functions and Organization is important
# Will want some of these functions when initializing a Playlist_Base
get_ipython().run_line_magic('run', 'PearPlaylistFunctions.ipynb')


# In[1]:



class Playlist_Base():
    def __init__(self, playlist_name = '', user_id = '', access_token = ''):
        self.playlist_name = playlist_name
        self.user_id = user_id
        self.access_token = access_token
        # Access_token from spotify_api has 'Bearer ' in front
        # Spotipy token built on not having Bearer, so ditch that
        self.sp_token = access_token[7:]
        try:
            sp = spotipy.Spotify(auth=self.sp_token)
            all_api_playlists = sp.user_playlists(user_id)
            self.spotipy_connection = sp
        except:
            print("Something went wrong hitting spotify API - did you provide the right token and username?")
        sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(user_id)
        
        self.generate_from_playlist_name(playlist_name)
        
    
    # takes a playlist_name and populates all other relevant variables of object
    # If a new playlist name is passed, it will overwrite all values
    def generate_from_playlist_name(self, playlist_name):
        self.playlist_name = playlist_name
        # Get all user's playlists from API PSI: Maybe there's a function that lets you hit API with playlist_name?
        sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(user_id)
        
        for api_playlist in all_api_playlists['items']:
            if(api_playlist['name'] == playlist_name):
                self.orig_playlist_dict = api_playlist
        
        # Now have the original playlist
        
        #TODO: Get features of this playlist, then build rec playlist then get features of that
        
        ### GET FEATURES OF ORIGINAL PLAYLIST
        orig_playlist_tracks_tmp = get_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)
        self.orig_playlist_tracks_df = get_track_features(orig_playlist_tracks_tmp, self.spotipy_connection)

        #self.track_features = get_track_features(track_df, playlist_name):
        ### CREATE RECS FROM PLAYLIST -- PFI: could make this function much more robust, look at artist/genre too
        # Get recommended tracks as dict
        rec_tracks_tmp = get_similar_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)
        self.rec_tracks_df = get_track_features(rec_tracks_tmp, self.spotipy_connection)
        
        ### GET FEATURES OF REC PLAYLIST -- PSI: make get_features function faster
        
        
        
    def print_playlist_name(self):
        print(self.playlist_name)


# In[ ]:




