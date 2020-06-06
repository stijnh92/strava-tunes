from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.conf import settings

import requests


def callback(request):
    code = request.GET.get('code')
    scope = request.GET.get('scope')

    response = requests.post('https://www.strava.com/oauth/token', json={
        'client_id': settings.STRAVA_API_CLIENT_ID,
        'client_secret': settings.STRAVA_API_SECRET,
        'code': code,
        'scope': scope
    })
    res = response.json()

    refresh_token = res['refresh_token']
    access_token = res['access_token']

    request.session['strava_access_token'] = access_token
    request.session['strava_refresh_token'] = refresh_token

    return HttpResponse('%s %s' % (refresh_token, access_token))

def activities(request):
    auth_token = request.session.get('strava_access_token')
    if not auth_token:
        # TODO: user has not yet authorized, redirect!
        return redirect('index')
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }
    req = requests.get('https://www.strava.com/api/v3/athlete/activities', headers=headers)
    all_activities = req.json()

    template = loader.get_template('strava/activities.html')
    context = {
        'activities': all_activities,
    }
    return HttpResponse(template.render(context, request))
