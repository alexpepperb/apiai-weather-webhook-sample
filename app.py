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
    print("this is an empty line")
    print(res)
    print("this is an empty line")
    r = make_response(res)
    print(r)
    print("this is an empty line")
    r.headers['Content-Type'] = 'application/json'
    print(r)
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    global targett
    targett = makeYqlQuery(req)
    if len(targett) == 0:
        res = emptyresponderr(req)
    else:
        res = trackpos(dictplay)
    return res

###result = requests.get(yql_url, headers=headers)

def trackpos(playdic):
    playl3 = {}
    for item in playdic:
        playl3[item] = sp.user_playlist_tracks('spotify_uk_', playlist_id=playdic[item], fields='items(track(name,album(name)))', offset=0, market=None)
    res = trackprint(playl3)
    return res

def trackprint(x):
    playl4 = {}
    for item in x:
        for i, tracks in enumerate(x[item]['items']):
            if tracks['track']['name'].lower().startswith(str(targett).lower()):
                playl4[len(playl4)+1] = "%s is number %s in %s" % (tracks['track']['name'], i + 1, item)
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
    global speech
    if len(playl4) == 0:
        speech = str("It doesn't look like that track is in any playlists")
    else:
        speech = str(playl4)
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": speech,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def emptyresponderr(req):
    global zspeech
    zspeech = str("That track wasn't recognised, try it again")
    
    print("Response:")
    print(zspeech)

    return {
        "speech": zspeech,
        "displayText": zspeech,
        "data": zspeech,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
