#!/usr/bin/env python
# coding: utf-8

# In[2]:


import spotipy
import spotipy.util as util
import pandas as pd 
import numpy as np
import copy
import sklearn
#from sklearn.decomposition import PCA
#from sklearn.preprocessing import StandardScaler
#import matplotlib.pyplot as plt

#from matplotlib import pyplot
#from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance_matrix
from .pearing_classes import Playlist_Base
from .pearing_core_functions import get_track_distances, create_playlist
import requests
import json
# In[2]:

def Pear_Playlists(playlist_name_1, playlist_name_2, access_token, user_id):
    ### INITIALIZE THINGS
    p1_base = Playlist_Base(playlist_name = playlist_name_1, user_id = user_id, access_token = access_token)
    p2_base = Playlist_Base(playlist_name = playlist_name_2, user_id = user_id, access_token = access_token)
    
    playlist_bases = [p1_base, p2_base]
    
    track_distances = get_track_distances(playlist_bases)
    
    
    ### FIND TRACKS
    # Look at each recommended track
    # Store each track in a df, with each column being the distance to one of the playlists
    p0_track_ids = playlist_bases[0].orig_playlist_tracks_df['track_id']
    p1_track_ids = playlist_bases[1].orig_playlist_tracks_df['track_id']




    # Make 3 lists to insert into data frame - PFI: need a more robust solution for more playlists
    track_ids = [None]*len(track_distances)
    p0_dist = [None]*len(track_distances)
    p1_dist = [None]*len(track_distances)
    for index, rec_track in track_distances.iterrows():
        # The index of each 'rec_track' is every column in the df (aka all original tracks)
        # We want to subset this to the specific playlists so that we can determine distance to each playlist
        track_ids[index] = rec_track['track_id']

        # the track ids in p0_track_ids should match the columns (aka index) of rec_track
        # Only look at those, then get avg dist
        p0_track_distances = rec_track[rec_track.index.isin(p0_track_ids)]
        p0_dist[index] = p0_track_distances.mean()

        p1_track_distances = rec_track[rec_track.index.isin(p1_track_ids)]
        p1_dist[index] = p1_track_distances.mean()

    cols = ['track_id', 'p0', 'p1']
    rec_tracks_to_playlists = pd.DataFrame({'track_id' : track_ids, 'p0': p0_dist, 'p1' : p1_dist})
    rec_tracks_to_playlists['avg_dist'] = rec_tracks_to_playlists.mean(axis = 1)
    final_tracks = rec_tracks_to_playlists.sort_values(by = ['avg_dist']).iloc[0:20]
    
    ### BUILD PLAYLIST
    sp = spotipy.Spotify(auth=access_token[7:])
    playlist_id = create_playlist(access_token, user_id.encode(), "SpotiPear_Playlist")
    # Now let's add some tracks
    track_ids_to_add = final_tracks['track_id']
    # TODO: Dynamically pull playlistid
    sp.user_playlist_add_tracks(user_id, playlist_id, track_ids_to_add)


# In[ ]:

def Pear_Playlists_tmp(playlist_name_1, playlist_name_2, access_token, user_id):
    ### INITIALIZE THINGS
    
    sp = spotipy.Spotify(auth=access_token[7:])
    playlist_id = create_playlist(access_token, user_id.encode(), "SpotiPear_Test_Playlist")
    # Now let's add some tracks
    


