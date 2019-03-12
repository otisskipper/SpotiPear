import spotipy
from .pearing_core_functions import get_tracks_from_playlist, get_track_features, get_similar_tracks_from_playlist


# Want an object that encapsulates our API pull of tracks and subsequent API pull of recommendations and features
# Playlist_Base Class
# Has:
# MUST BE SPECIFIED AT CREATE TIME

# user_id - spotify user id
# access_token - returned from spotify api

# playlist_name - string

# From that generate:
# orig_playlist_dict
# orig_playlist_tracks_df - includes features
# rec_tracks_df - includes features


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
            all_api_playlists = sp.user_playlists(self.user_id)
            self.spotipy_connection = sp
        except:
            print("Something went wrong hitting spotify API - did you provide the right token and username?")
        sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(self.user_id)
        
        self.generate_from_playlist_name(playlist_name)
        
    
    # takes a playlist_name and populates all other relevant variables of object
    # If a new playlist name is passed, it will overwrite all values
    def generate_from_playlist_name(self, playlist_name):
        self.playlist_name = playlist_name
        # Get all user's playlists from API 
        sp = spotipy.Spotify(auth=self.sp_token)
        all_api_playlists = sp.user_playlists(self.user_id)
        
        for api_playlist in all_api_playlists['items']:
            if(api_playlist['name'] == playlist_name):
                self.orig_playlist_dict = api_playlist
        
        # Now have the original playlist - if a user has 2 playlists of same name this will pick whichever playlist appears last in the list
        
        
        ### GET FEATURES OF ORIGINAL PLAYLIST
        orig_playlist_tracks_tmp = get_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)
        self.orig_playlist_tracks_df = get_track_features(orig_playlist_tracks_tmp, self.access_token, self.user_id)

        
        ### CREATE RECS FROM PLAYLIST -- PFI: could make this function much more robust, look at artist/genre too
        
        # Get recommended tracks as dict
        rec_tracks_tmp = get_similar_tracks_from_playlist(self.user_id, self.orig_playlist_dict, self.spotipy_connection)
        self.rec_tracks_df = get_track_features(rec_tracks_tmp, self.access_token, self.user_id)
        

        
