import hashlib

from django.http import HttpResponse

import requests
from django.shortcuts import redirect
from django.template import loader
from django.conf import settings


def callback(request):
    token = request.GET.get('token')

    api_key = settings.LAST_FM_API_KEY
    secret = settings.LAST_FM_API_SECRET
    method = 'auth.getSession'
    api_signature = hashlib.md5(f"api_key{api_key}method{method}token{token}{secret}".encode('utf-8')).hexdigest()
    payload = {
        'api_key': api_key,
        'api_sig': api_signature,
        'token': token,
        'method': method,
        'format': 'json'
    }
    headers = {
        'user-agent': 'Running-Beats'
    }

    print(payload)

    req = requests.get('http://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
    response = req.json()
    print(response)

    request.session['last_fm_token'] = response['session']['key']
    request.session['last_fm_user'] = response['session']['name']

    return HttpResponse(token)

def history(request):
    user = request.session.get('last_fm_user')
    if not user:
        # TODO: no user defined, redirect!
        return redirect('index')

    api_key = settings.LAST_FM_API_KEY

    req = requests.get(f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json')
    response = req.json()

    tracks = response['recenttracks']['track']
    print(tracks)

    template = loader.get_template('lastfm/history.html')
    context = {
        'tracks': tracks
    }
    return HttpResponse(template.render(context, request))
