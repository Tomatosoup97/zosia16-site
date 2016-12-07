from urllib.parse import urlencode

from django.shortcuts import render
from django.conf import settings

from .models import Zosia


GAPI_PLACE_BASE_URL = "https://www.google.com/maps/embed/v1/place"


def index(request):
    zosia = Zosia.objects.find_active()
    context = {
        'zosia': zosia,
    }
    if zosia:
        query = {
            'key': settings.GAPI_KEY,
            'q': zosia.place.address,
        }
        context['gapi_place_src'] = GAPI_PLACE_BASE_URL + '?' + urlencode(query)
    return render(request, 'conferences/index.html', context)
