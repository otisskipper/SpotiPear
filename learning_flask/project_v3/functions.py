def custom_add(n1, n2):
	return str(int(n1) + int(n2))

def test1():
	return 'test'


def spotify_login():
	import spotipy
	# TODO: Turn into Function
	scope = 'user-library-read'
	client_id ='a63ddab3e3d147898a0df1d5658f9ee9'
	client_secret ='226f21e7e723484f909f768fdadada7c'
	redirect_uri ='http://localhost/'

	# Profile url: https://open.spotify.com/user/22r6slwbns4u7hkhn3hjhjhyi?si=MX4wzJ3PQeiH_7IKIHHrMA
	# Find way so that users don't have to get their link
	username = '22r6slwbns4u7hkhn3hjhjhyi'
	token = spotipy.util.prompt_for_user_token(username, scope = scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
	
	return token


def spotify_login_new():
	import spotipy
	# TODO: Turn into Function
	scope = 'user-library-read'
	client_id ='a63ddab3e3d147898a0df1d5658f9ee9'
	client_secret ='226f21e7e723484f909f768fdadada7c'
	redirect_uri ='http://localhost/'

	# Profile url: https://open.spotify.com/user/22r6slwbns4u7hkhn3hjhjhyi?si=MX4wzJ3PQeiH_7IKIHHrMA
	# Find way so that users don't have to get their link
	username = '22r6slwbns4u7hkhn3hjhjhyi'
	token = spotipy.util.prompt_for_user_token(username, scope = scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri)
	
	return username