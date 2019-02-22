#import config 
from flask import Flask, render_template, request, redirect, url_for, make_response


import spotipy
#import spotipy.util as util
import numpy
import pandas as pd 
from functions import get_access_token
import requests
#import numpy as np
#import copy
#from sklearn.decomposition import PCA
#from sklearn.preprocessing import StandardScaler
#import matplotlib.pyplot as plt

#from matplotlib import pyplot
#from mpl_toolkits.mplot3d import Axes3D
#from scipy.spatial import distance_matrix

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():

    Cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
        'Price': [22000,25000,27000,35000]
        }

    df = pd.DataFrame(Cars, columns= ['Brand', 'Price'])

    my_str = df.to_string()
    return my_str
    #return render_template("about.html")

@app.route("/logged_in")
def logged_in():
    code = request.args.get('code')
    access_token = get_access_token(code, request, app.config['AUTHORIZATION'], requests)
    return access_token
    #return render_template("logged_in.html")


@app.route("/button")
def button():
    return render_template("button.html")

@app.route("/login")
def login():
    callback_url = request.url_root + 'logged_in'
    base_url = 'https://accounts.spotify.com/en/authorize?client_id=' + app.config['CLIENT_ID'] + '&response_type=code&redirect_uri=' + callback_url + '&scope=user-read-email%20playlist-read-private%20user-follow-read%20user-library-read%20user-top-read%20playlist-modify-private%20playlist-modify-public&state=34fFs29kd09'
    # this is how we set the Cookie when its a Redirect instead of return_response
    # https://stackoverflow.com/questions/12272418/in-flask-set-a-cookie-and-then-re-direct-user
    # response = make_response(redirect(base_url, 302))
    # response = make_response(redirect(base_url, 302))
    # response.set_cookie('time_range', request.args.get('time_range'))
    response = make_response(redirect(base_url, 302))
    return response


if __name__ == "__main__":
    app.run(debug=True)


# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import logging

# from flask import Flask
# import numpy as np
# import pandas

# app = Flask(__name__)


# @app.route('/')
# def calculate():
#     return_str = ''
#     x = np.array([[1, 2], [3, 4]])
#     y = np.array([[5, 6], [7, 8]])

#     return_str += 'x: {} , y: {}<br />'.format(str(x), str(y))

#     # Multiply matrices
#     return_str += 'x dot y : {}'.format(str(np.dot(x, y)))
#     return return_str


# @app.errorhandler(500)
# def server_error(e):
#     logging.exception('An error occurred during a request.')
#     return """
#     An internal error occurred: <pre>{}</pre>
#     See logs for full stacktrace.
#     """.format(e), 500


# if __name__ == '__main__':
#     # This is used when running locally. Gunicorn is used to run the
#     # application on Google App Engine. See entrypoint in app.yaml.
#     app.run(host='127.0.0.1', port=8080, debug=True)
