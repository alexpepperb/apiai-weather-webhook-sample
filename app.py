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
dictplay = {'This Is How We Do' : '5rZjd5MqTPPCtrpX2hvKHt', 'You Can Do It' : '3SWuW0hxd6URGfmYFgz9Da', 'Dancehall Queen' : '2XFhCi8j0RPvxsENIeecMJ', 'Massive Dance Hits' : '7wUUwoxU2S6BRKA2bDPYKD', 'Focus On The Remix' : '2uq659dHfDDolMijdmtT4e', 'Teen Pop Party' : '1WXwg9vAfbVcotgkN69UFg', 'Carnival' : '2hOxbFkkVIrC3UAl111sQN', 'Summer Anthems' : '2hTH54LKZRZHkzKwmKBD0w', 'Who We Be' : '4ZwGxXnrDHsMnWjrhofaaR', 'Totally Tropical House' : '5IqZyShbVqwR9GQ1FVmHCT', 'New Dance Revolution' : '27PF19QnWbJAwfY4dLFBQu', 'Grime Instrumentals' : '6e0qWsLYofNNlml9jvJau8', 'All Night Dance Party' : '3pWL5FdzK7xyUoSzzQzjLx', 'Rap UK' : '2HBbGDH1fIhygx7XWHs6tL', 'Live To Run' : '6HeKiUlYhtogMiMb1uaIZh', 'Happy Pop Hits' : '5MaioFUFxRYTObp7fUfphO', 'One Week One Playlist' : '3nUU3opyeRtDx6Jiyeo7ty', 'Hot Hits UK' : '6FfOZSAN3N6u7v81uS7mxZ', 'New Pop Revolution' : '534FHdUH9qaG1WxiqsOnb9', 'Summer Hits' : '6QcSOqFBwxfJPwVV4Ybjp6', 'Rap Workout' : '1d2sDCH9B9rwasXNmQbKrj', 'The Pop List' : '1Tv8NFvQY2aRuGi2JrOeyN', 'Alternative Hip-Hop' : '4zzNotCyHYZY0SGQBjko7w', '#MondayMotivation' : '1o2lkeg4vZRfpNL3dgP5zv', 'New Music Friday UK' : '6LY8RIt0Wg6IkpJBtxP2xu', 'Sweet Soul Sunday' : '4SojeGPKh2YVnynxs0MQgH', 'A Fun Workout' : '05FXFFPuiL69mi1m55q8yM', 'Chilled Pop Hits' : '3zn59U9FkTNzQwE0T5mW4I', 'All New All Now' : '3KPoDD9YsxfsIN1YVdlnNP', 'Remixing The Deep' : '5gwcsFHPJCpOaObq48Sixk', 'The Other List' : '33yjWFG5onxZu3HdIzO1Zu', 'Ibiza Sunset' : '0bBpUSe725j2EBy1dvSwK8', 'The Office Stereo' : '0v6rFvR3SDoynXcTpQMO0n', 'Trending On TV' : '1n73tGPnX067UzMleUXLtC', 'Spotify + Chill' : '1JNce9gdMknj1hw5eynsLn', 'Easy' : '1uR5XIi29PylxTvHs3cVPP', 'Pop Acoustic' : '4gcaLiHMzbb44aXVrSiJx5', 'Acoustic Rock' : '4IAnj0lvQc5NQsVS8gt3Iw', 'Very Nearly Nashville' : '0gGCROfxWFpk9MXdepWyLl', 'Mellow Pop' : '6CVvJhUjiYjZnuC5xu0lqH', 'Heartbreaker' : '6q8divpHUKfUhUMzlx8vGo', 'Revision Ballads' : '7bhn4nYiYe9ygaFLGXLuih', '4am Comedown' : '3NFZhkxiNzfrUWETRF7rqc', 'The Stress Buster' : '6JC48D3eRvkUHACDtyu0Gs', 'Massive Drum & Bass' : '4CnKpTkDO51sMVplwnh5Ij', 'The Moon is Calling' : '5xYXO93XWSBJS46X67byvn', 'Lost In The Woods' : '7oJfxtT97OHhIAqNnWknhI', 'Run N Bass' : '70DLF4cCN33LfiXFwd7Adp', 'The Indie List' : '5jVou6V5D3KjP8uk7hj1cu', 'Hot New Bands' : '5Dhb1Bm6xbD3Ig4VHO5y33', 'Sad Songs' : '0ApL3HCGSTLQhXIcQqIMVZ', 'Rocked.' : '3jgQOc0rIN5POlnuVof0ck', 'Songs For Sleeping' : '5KfP2yuAMWB4hRf271loNC', 'The Most Beautiful Songs In The World' : '6y3CuT7MDDoPNXaD69frug'}


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
        speech = ""
        for i in playl4:
            speech = speech + "\n" + str(playl4[i])
    
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
