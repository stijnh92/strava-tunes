from strava import utils as strava_utils
from lastfm import utils as lastfm_utils

from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('webapp/index.html')
    context = {
        'strava_authorization_url': strava_utils.get_authorization_url(),
        'lastfm_authorization_url': lastfm_utils.get_authorization_url()
    }
    return HttpResponse(template.render(context, request))
