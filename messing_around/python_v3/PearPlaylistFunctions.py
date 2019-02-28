#!/usr/bin/env python
# coding: utf-8

# In[2]:


import spotipy
import spotipy.util as util
import pandas as pd 
import numpy as np
import copy
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import distance_matrix


# In[2]:


# Given a username and a playlist_dict, generate a dataframe of 'similar' songs
#PFI: This function could be way more robust, looking at a artists/genres as well as randomizing/subsampling to improve speed

# TODO: Get Recommendations off of Recommendations (probably only want to do recursively once)
def get_similar_tracks_from_playlist(username_var, playlist_var, spotipy_connection):
    top_level_tracks = spotipy_connection.user_playlist(username_var, playlist_var['id'],
                    fields="tracks,next")
    second_level_tracks = top_level_tracks['tracks']
    playlist_var_track_ids = [None]*len(second_level_tracks['items'])
    playlist_var_artist_ids = [None]*len(second_level_tracks['items'])
    # playlist_1_genre_ids = [None]*len(second_level_tracks['items'])
    for i, item in enumerate(second_level_tracks['items']):
        cur_track = item['track']
        playlist_var_track_ids[i] = cur_track['id']
#        playlist_var_artist_ids[i] = cur_track['artists'][0]['id']


## Sometimes we get a track with a "none" value, get rid of these (this could reset indexing, don't rely on indices)
    playlist_var_track_ids = [x for x in playlist_var_track_ids if x != None]

    rec_tracks_list = [None]*int((len(playlist_var_track_ids)/5)-1)
    for i in range(0,len(rec_tracks_list)):
        rec_tracks_list[i] = spotipy_connection.recommendations(seed_tracks = playlist_var_track_ids[i*5:(i+1)*5])
        
    # rec_tracks_list is a list of lists, each sublist has a track
    # extract out to a single list
    rec_tracks_list_full = [None]*20*len(rec_tracks_list)

    # Iterate over all sets of recommendations from groups of 5 songs
    for i, rec_set in enumerate(rec_tracks_list):

        # Iterate over every track
        for j, tracks in enumerate(rec_set['tracks']):
            rec_tracks_list_full[i*20 + j] = tracks['id']
            #print(tracks['artists'][0]['name'], ': ', tracks['name'], sep = '')

    all_track_ids = pd.DataFrame(np.array(rec_tracks_list_full))
    all_track_ids.columns=['track_id']
    return all_track_ids


# In[ ]:





# In[2]:


def get_track_features(track_df, spotipy_connection):

    track_df_var = copy.deepcopy(track_df)
    new_cols = list(['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])

    # Create all new columns for feature types
    for col in new_cols:
        # Initialize Column as empty
        track_df_var[col] = np.nan
        # Run over each row
    for i in range(0, len(track_df_var)):
        # Get features for current song
        cur_track_features = spotipy_connection.audio_features(track_df_var['track_id'][[i]])
        #Insert specific feature into column
        #TODO: This currently calls the sp.audio_features like 10 times for each song (since I do it for each row)
        for col in new_cols:
            track_df_var[col].iloc[i] = cur_track_features[0][col]
    
    return track_df_var


# In[5]:


# Given a playlist (and the username of its owner) return a dataframe of the track IDs

def get_tracks_from_playlist(username, playlist, spotipy_connection):
    
    # Do some stuff to account for the hierarchical structure of what we get back
    top_level_tracks = spotipy_connection.user_playlist(username, playlist['id'],
                    fields="tracks,next")

    second_level_tracks = top_level_tracks['tracks']
    
    # Initialize empty list for track_ids
    playlist_track_ids = [None]*len(second_level_tracks['items'])
    
    #PFI: could do something similar for artist/genre and Pear on those as well
    #playlist_var_artist_ids = [None]*len(second_level_tracks['items'])
    # playlist_1_genre_ids = [None]*len(second_level_tracks['items'])
    
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


# In[ ]:





# In[4]:


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


# In[2]:


# PCA
# Given List of N dfs with tracks as rows and audio features as columns
# Union all, do PCA (so that they're all on the same scale) then separate out into list of DFs

def pca_merge(feature_dfs):
    all_features_tmp = pd.DataFrame(columns = feature_dfs[0].columns)
    all_features_tmp['playlist_iter'] = None
    feature_dfs_copy = copy.deepcopy(feature_dfs)
    for i, playlist_features in enumerate(feature_dfs_copy):
        playlist_features['playlist_iter'] = i
        all_features_tmp = all_features_tmp.append(playlist_features)



    # Mode and Key make PCA look weird (at least for graphing) - take them out for time being
    # PFI: Take a look at this again, maybe they're useful, but just not in visualization
    all_features = all_features_tmp.drop(['mode', 'key'], axis = 1).reset_index()

    # Actual PCA
    x = all_features.drop(['playlist_iter', 'track_id'], axis = 1)
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    #TODO: Adjust to dynamically create table so that we can have n principal components
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents
                 , columns = ['principal component 1', 'principal component 2', 'principal component 3'])
    playlists_finalDf = pd.concat([principalDf,  all_features[['playlist_iter']]], axis = 1)

    return playlists_finalDf


# In[3]:


#Given set of Playlist_bases objects, get a distance matrix of all tracks to all other tracks (will be redundancies)
# Assumes the rec_tracks_df of all base playlists is the same
def get_track_distances_tmp(playlist_bases):

    # Need a df with all tracks as rows
    # All features as columns
    
    # Create empty data frame to union results onto
    all_rec_tracks_tmp = pd.DataFrame(columns = playlist_bases[0].rec_tracks_df.columns)
    all_orig_tracks_tmp = pd.DataFrame(columns = playlist_bases[0].orig_playlist_tracks_df.columns)
    
    for playlist_base in playlist_bases:
        rec_tracks_df = playlist_base.rec_tracks_df
        all_rec_tracks_tmp = all_rec_tracks_tmp.append(rec_tracks_df)
        orig_playlist_tracks_df = playlist_base.orig_playlist_tracks_df
        all_orig_tracks_tmp = all_orig_tracks_tmp.append(orig_playlist_tracks_df)
        
    # Mode & Key did bad stuff in early analysis
    all_rec_tracks = all_rec_tracks_tmp.reset_index().drop(['index','mode', 'key'], axis = 1)
    all_orig_tracks = all_orig_tracks_tmp.reset_index().drop(['index','mode', 'key'], axis = 1)
    
    # Now get all original tracks, compare distance 


    all_tracks = all_rec_tracks.append(all_orig_tracks).reset_index().drop(['index'], axis = 1)
    
    all_tracks_scaled = pd.DataFrame(StandardScaler().fit_transform(all_tracks.drop(['track_id'], axis = 1)))

    
    all_rec_tracks_scaled = all_tracks_scaled.iloc[0:len(all_rec_tracks)]
    all_rec_tracks_scaled['track_id'] = all_rec_tracks['track_id']
    all_orig_tracks_scaled = all_tracks_scaled.iloc[len(all_rec_tracks):all_tracks_scaled.shape[0]].reset_index().drop(['index'], axis = 1)
    all_orig_tracks_scaled['track_id'] = all_orig_tracks['track_id']
    
    all_tracks_scaled['track_id'] = all_tracks['track_id']
    ### Normalize that shit before doing the distance matrix, have to put in same df to normalize
    ### 
#    dist_matrix = pd.DataFrame(distance_matrix(all_rec_tracks.drop(['track_id'], axis = 1).values, all_orig_tracks.drop(['track_id'], axis = 1).values))
    dist_matrix = pd.DataFrame(distance_matrix(all_rec_tracks_scaled.drop(['track_id'], axis = 1).values, all_orig_tracks_scaled.drop(['track_id'], axis = 1).values))
    
    # Now have a distance matrix whose rows are all of our recommended tracks
    # Columns are all original tracks, and values are the distance between the songs (after all were normalized together)
    # Make the column names and row names the actual track_ids 
    dist_matrix.columns = all_orig_tracks['track_id']
    dist_matrix.insert(0, 'track_id', all_rec_tracks['track_id'])
    
    
    return dist_matrix


# In[6]:


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
    return  playlist_id #full_pl


# In[1]:


def Pear_Playlists(playlist_name_1, playlist_name_2, access_token, user_id):
    ### INITIALIZE THINGS
    p1_base = Playlist_Base(playlist_name = p1_name, user_id = user_id, access_token = access_token)
    p2_base = Playlist_Base(playlist_name = p2_name, user_id = user_id, access_token = access_token)
    
    playlist_bases = [p1_base, p2_base]
    
    track_distances = get_track_distances_tmp(playlist_bases)
    
    
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
    playlist_id = create_playlist(access_token, user_id.encode(), "SpotiPear_Test_Playlist")
    # Now let's add some tracks
    track_ids_to_add = final_tracks['track_id']
    # TODO: Dynamically pull playlistid
    sp.user_playlist_add_tracks(user_id, playlist_id, track_ids_to_add)


# In[ ]:




