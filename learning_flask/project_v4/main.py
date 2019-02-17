import config
from flask import Flask, render_template, request, redirect, url_for, make_response


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

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logged_in")
def logged_in():
    return render_template("logged_in.html")


@app.route("/button")
def button():
    return render_template("button.html")

@app.route("/login")
def login():
	var = "test2"
	callback_url = request.url_root + 'logged_in'
	base_url = 'https://accounts.spotify.com/en/authorize?client_id=' + config.client_id + '&response_type=code&redirect_uri=' + callback_url + '&scope=user-read-email%20playlist-read-private%20user-follow-read%20user-library-read%20user-top-read%20playlist-modify-private%20playlist-modify-public&state=34fFs29kd09'
    # this is how we set the Cookie when its a Redirect instead of return_response
    # https://stackoverflow.com/questions/12272418/in-flask-set-a-cookie-and-then-re-direct-user
    # response = make_response(redirect(base_url, 302))
    # response = make_response(redirect(base_url, 302))
    # response.set_cookie('time_range', request.args.get('time_range'))
	response = make_response(redirect(base_url, 302))
	return response


if __name__ == "__main__":
    app.run(debug=True)
