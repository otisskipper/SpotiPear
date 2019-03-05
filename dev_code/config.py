import base64
CLIENT_ID = 'a63ddab3e3d147898a0df1d5658f9ee9'
CLIENT_SECRET = '226f21e7e723484f909f768fdadada7c'
#authorization = 'Basic ' + base64.b64encode(client_id + ':' + client_secret)
#authorization = 'Basic ' + base64.b64encode(authorization_tmp.encode("utf-8")).decode("utf-8")
SECRET_KEY = '226f21e7e723484f909f768fdadada7c'
AUTHORIZATION = 'Basic ' + (base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())).decode("utf-8")