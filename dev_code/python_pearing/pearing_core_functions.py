
import spotipy

import pandas as pd 
import numpy as np
import copy

import sklearn
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance_matrix
import requests
import json
import math



# Given a username and a playlist_dict, generate a dataframe of 'similar' songs
#PFI: This function could be way more robust, looking at a artists/genres as well as randomizing/subsampling to improve speed

# PFI: Get Recommendations off of Recommendations (probably only want to do recursively once)
def get_similar_tracks_from_playlist(username_var, playlist_var, spotipy_connection):
    # Use spotipy library to get the user's playlist and then parse JSON and get track ids
    top_level_tracks = spotipy_connection.user_playlist(username_var, playlist_var['id'],
                    fields="tracks,next")
    second_level_tracks = top_level_tracks['tracks']


    playlist_var_track_ids = [None]*len(second_level_tracks['items'])
    
    for i, item in enumerate(second_level_tracks['items']):
        cur_track = item['track']
        playlist_var_track_ids[i] = cur_track['id']

    ## Sometimes we get a track with a "none" value, get rid of these (this could reset indexing, don't rely on indices)
    playlist_var_track_ids = [x for x in playlist_var_track_ids if x != None]

    # Pull recommendations and build list of more recommendations
    # Must be a list of 5 SpotifyIDs 
    # PFI: Currently I'm passing track_id, but could pass artist, playlist, etc...
    rec_tracks_list = [None]*int((len(playlist_var_track_ids)/5)-1)
    for i in range(0,len(rec_tracks_list)):
        rec_tracks_list[i] = spotipy_connection.recommendations(seed_tracks = playlist_var_track_ids[i*5:(i+1)*5])
        
    # rec_tracks_list is a list of lists, each sublist has a track
    # extract out to a single list
    # be default each recommendation call to API sends back 20 recs
    rec_tracks_list_full = [None]*20*len(rec_tracks_list)

    # Iterate over all sets of recommendations from groups of 5 SpotifyIDs
    for i, rec_set in enumerate(rec_tracks_list):

        # Iterate over every track
        for j, tracks in enumerate(rec_set['tracks']):
            rec_tracks_list_full[i*20 + j] = tracks['id']
            

    all_track_ids = pd.DataFrame(np.array(rec_tracks_list_full))
    all_track_ids.columns=['track_id']
    return all_track_ids




# Get the features for every song in a dataframe
def get_track_features(track_df, access_token, user_id):

    cols_to_keep = list(['track_id','danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
    
    # Can only get up to 100 songs at a time from API
    # make empty df, iterate over every 100 songs and append
    track_features_df = pd.DataFrame(columns = cols_to_keep)
    track_list = track_df['track_id'].tolist()
    api_headers = {'Authorization': access_token}
    for i in range(0,(math.ceil(len(track_list)/100))):
        track_list_tmp = track_list[i*100:(i+1)*100]
        api_url = 'https://api.spotify.com/v1/audio-features/?ids=' + ','.join(track_list_tmp)
        api_get_response = requests.get(api_url, headers = api_headers )
        track_features_json = api_get_response.json()
        track_features_df_tmp = pd.DataFrame(track_features_json['audio_features'])
        track_features_df_tmp['track_id'] = track_features_df_tmp['id']
        track_features_df_tmp = track_features_df_tmp[cols_to_keep]
        track_features_df = track_features_df.append(track_features_df_tmp)

    return track_features_df



# Given a playlist (in json format) (and the username of its owner) return a dataframe of the track IDs

def get_tracks_from_playlist(username, playlist, spotipy_connection):
    
    # Do some stuff to account for the hierarchical structure of what we get back
    top_level_tracks = spotipy_connection.user_playlist(username, playlist['id'],
                    fields="tracks,next")

    second_level_tracks = top_level_tracks['tracks']
    
    # Initialize empty list for track_ids
    playlist_track_ids = [None]*len(second_level_tracks['items'])
    
    #PFI: could do something similar for artist/genre and Pear on those as well
    #playlist_var_artist_ids = [None]*len(second_level_tracks['items'])
    #playlist_1_genre_ids = [None]*len(second_level_tracks['items'])
    
    for i, item in enumerate(second_level_tracks['items']):
        cur_track = item['track']
        playlist_track_ids[i] = cur_track['id']
        #playlist_var_artist_ids[i] = cur_track['artists'][0]['id']


    # Sometimes we get a track with a "none" value, get rid of these 
    playlist_track_ids = [x for x in playlist_track_ids if x != None]
    # Make it a DF
    to_return = pd.DataFrame(np.array(playlist_track_ids))
    to_return.columns=['track_id']
    return to_return





# Given a set of chosen playlist names, and the returned API call of all the user's playlists (dict of each playlist)
# returns a list of individual playlist (dict) objects matching the names provided
def get_api_playlists_from_names(chosen_playlist_names, all_api_playlists):
    # Initialize List to place playlists in
    chosen_api_playlists = [None]*len(chosen_playlist_names)
    
    # Iterate over each name, then all items in api, then check for match (PSI: double for loops are bad?)
    for i, playlist_name in enumerate(chosen_playlist_names):
        for api_playlist in all_api_playlists['items']:
            if(api_playlist['name'] == playlist_name):
                chosen_api_playlists[i] = api_playlist
    
    return chosen_api_playlists 



#Given set of Playlist_bases objects, get a distance matrix of all tracks to all other tracks (will be redundancies)
# Assumes the rec_tracks_df of all base playlists has the same columns
def get_track_distances(playlist_bases):

    # Need a df with all tracks as rows
    # And All features as columns
    
    # Create empty data frame to union results onto
    all_rec_tracks_tmp = pd.DataFrame(columns = playlist_bases[0].rec_tracks_df.columns)
    all_orig_tracks_tmp = pd.DataFrame(columns = playlist_bases[0].orig_playlist_tracks_df.columns)
    
    for playlist_base in playlist_bases:
        rec_tracks_df = playlist_base.rec_tracks_df
        all_rec_tracks_tmp = all_rec_tracks_tmp.append(rec_tracks_df)
        orig_playlist_tracks_df = playlist_base.orig_playlist_tracks_df
        all_orig_tracks_tmp = all_orig_tracks_tmp.append(orig_playlist_tracks_df)
        
    # Mode & Key did bad stuff in early analysis so remove them
    all_rec_tracks = all_rec_tracks_tmp.reset_index().drop(['index','mode', 'key'], axis = 1)
    all_orig_tracks = all_orig_tracks_tmp.reset_index().drop(['index','mode', 'key'], axis = 1)
    
    
    # We combined all dataframes into 1 so that we could scale them
    # We can't individually scale the dataframes separately (avg of df1 is 3, avg of df2 is 4 but those both individually scale to 0)
    # So need to scale all songs together
    all_tracks = all_rec_tracks.append(all_orig_tracks).reset_index().drop(['index'], axis = 1)
    
    all_tracks_scaled = pd.DataFrame(StandardScaler().fit_transform(all_tracks.drop(['track_id'], axis = 1)))
    
    # Now get all original tracks, compare distance 
    all_rec_tracks_scaled = all_tracks_scaled.iloc[0:len(all_rec_tracks)]
    all_rec_tracks_scaled['track_id'] = all_rec_tracks['track_id']
    all_orig_tracks_scaled = all_tracks_scaled.iloc[len(all_rec_tracks):all_tracks_scaled.shape[0]].reset_index().drop(['index'], axis = 1)
    all_orig_tracks_scaled['track_id'] = all_orig_tracks['track_id']
    
    all_tracks_scaled['track_id'] = all_tracks['track_id']
    
    dist_matrix = pd.DataFrame(distance_matrix(all_rec_tracks_scaled.drop(['track_id'], axis = 1).values, all_orig_tracks_scaled.drop(['track_id'], axis = 1).values))
    
    # Now have a distance matrix whose rows are all of our recommended tracks
    # Columns are all original tracks, and values are the distance between the songs (after all were normalized together)
    # Make the column names and row names the actual track_ids 
    dist_matrix.columns = all_orig_tracks['track_id']
    dist_matrix.insert(0, 'track_id', all_rec_tracks['track_id'])
    
    
    return dist_matrix



# Leverage spotipy here instead, could be more concise

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
 
    return  playlist_id #full_pl





