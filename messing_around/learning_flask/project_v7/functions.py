import requests

def get_access_token(code, request, authorization, requests):
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