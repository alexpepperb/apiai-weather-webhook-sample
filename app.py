#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "'https://api.spotify.com/v1/artists/"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + yql_query + "/top-tracks?country=GB'"
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer BQC0YxkTAZx8Cu9GaIY3ENZ6-2-ZF8lEIWrLQoazuF_S15GIhe0_w3sbS48ur6lTJomu21w0q418PDiVANuFLDMrUW_igTnp_PHaQw6DWSEskK8MLAaMguwXn3VeY3X0cs8ACVSUah64E2fN54vAgo4',
}
    result = urllib.request.urlopen('https://api.spotify.com/v1/artists/04gDigrS5kc9YWfZHwBETP/top-tracks?country=GB', headers=headers).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res

###result = requests.get(yql_url, headers=headers)


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("uriartist")
    if city is None:
        return None
    
    return city


def makeWebhookResult(data):
    tracks = data.get('tracks')
    if tracks is None:
        return {}

    album = tracks.get('album')
    if result is None:
        return {}
    
    artists = album.get('artists')
    if result is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "The top track for " + artists.get('name') + " is " + album.get('name')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
