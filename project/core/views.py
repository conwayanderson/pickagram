from django.template.response import TemplateResponse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from instagram import client, subscriptions


unauthenticated_api = client.InstagramAPI(**settings.INSTAGRAM_CONFIG)


def home(request):
    access_token = request.session.get('access_token')
    instagram_oauth_url = None

    if access_token:
        api = client.InstagramAPI(access_token=access_token[0])
        popular = api.media_popular(count=2)
    else:
        instagram_oauth_url = unauthenticated_api.get_authorize_url(
            scope=["likes"])

        api = client.InstagramAPI(
            client_id=settings.INSTAGRAM_CONFIG['client_id'],
            client_secret=settings.INSTAGRAM_CONFIG['client_secret'])
        popular = api.media_popular(count=2)

    return TemplateResponse(request, 'core/home.html', {
        'instagram_oauth_url': instagram_oauth_url,
        'access_token': access_token,
        'popular': popular,
        'previous_vote': None,
    })


def like(request, media_id):
    access_token = request.session.get('access_token')
    if not access_token:
        messages.error(request, 'Please login with Instagram before voting!')
    else:
        api = client.InstagramAPI(access_token=access_token[0])
        api.like_media(media_id)
    
    return HttpResponseRedirect(reverse('core:home'))


def oauth_callback(request):
    code = request.GET.get('code')
    if code:
        access_token = unauthenticated_api.exchange_code_for_access_token(code)
        request.session['access_token'] = access_token
        if not access_token:
            messages.error(request, 'Could not get access token.')
    else:
        messages.error(request, 'You must have an oauth access code to login, '
                                'no code was provided.')

    return HttpResponseRedirect(reverse('core:home'))


def oauth_logout(request):
    if request.session.get('access_token'):
        request.session['access_token'] = None

    messages.success(request, 'You have successfully logged out.')

    return HttpResponseRedirect(reverse('core:home'))
