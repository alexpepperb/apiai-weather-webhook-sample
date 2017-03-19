#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import spotipy

from flask import Flask
from flask import request
from flask import make_response
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials("36919004726b47d4b7ecbef19aebabc8","a074aa09a1664c79a45c35b4526d67f4","http://localhost:1410/")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
dictplay = {'The Pop List' : '1Tv8NFvQY2aRuGi2JrOeyN', 'Teen Pop Party' : '1WXwg9vAfbVcotgkN69UFg', 'Chilled Pop Hits' : '3zn59U9FkTNzQwE0T5mW4I', 'Happy Pop Hits' : '5MaioFUFxRYTObp7fUfphO', 'Pop Acoustic' : '4gcaLiHMzbb44aXVrSiJx5'}

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    targett = str("Be The One")
    if targett is None:
        return {}
    data = trackpos(dictplay)
    

###result = requests.get(yql_url, headers=headers)

def trackpos(playdic):
    playl3 = {}
    for item in playdic:
        playl3[item] = sp.user_playlist_tracks('spotify_uk_', playlist_id=playdic[item], fields='items(track(name,album(name)))', offset=0, market=None)
        trackprint(playl3)

def trackprint(x):
    playl4 = {}
    for item in x:
        for i, tracks in enumerate(x[item]['items']):
            if tracks['track']['name'].lower().startswith(str(targett).lower()):
                playl4[tracks] = "%s is number %s in %s" % (tracks['track']['name'], i + 1, item)
    res = responderr(playl4)
    return res
        
def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("uriartist")
    if city is None:
        return None
    
    return city

def responderr(playl4):
    print("Response:")
    print(playl4)

    return {
        "speech": str(playl4),
        "displayText": speech,
        "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
