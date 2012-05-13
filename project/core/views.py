from django.template.response import TemplateResponse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from instagram import client, subscriptions


unauthenticated_api = client.InstagramAPI(**settings.INSTAGRAM_CONFIG)


def home(request):
    if request.session.get('access_token'):
        return HttpResponseRedirect(reverse('core:pick'))

    instagram_oauth_url = unauthenticated_api.get_authorize_url(
        scope=["likes"])
    return TemplateResponse(request, 'core/home.html', {
        'instagram_oauth_url': instagram_oauth_url,
    })


def pick(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return HttpResponseRedirect(reverse('core:home'))

    api = client.InstagramAPI(access_token=access_token[0])
    popular = api.media_popular(count=2)

    return TemplateResponse(request, 'core/pick.html', {
        'popular': popular,
        'access_token': access_token,
        'counter': request.session.get('counter'),
    })


def like(request, media_id):
    access_token = request.session.get('access_token')
    if not access_token:
        return HttpResponseRedirect(reverse('core:home'))

    api = client.InstagramAPI(access_token=access_token[0])
    api.like_media(media_id)
    if request.session.get('counter'):
        request.session['counter'] += 1
    else:
        request.session['counter'] = 1
    
    return HttpResponseRedirect(reverse('core:pick'))


def oauth_callback(request):
    error = False
    code = request.GET.get('code')
    if code:
        access_token = unauthenticated_api.exchange_code_for_access_token(code)
        request.session['access_token'] = access_token
        if not access_token:
            error = True
            messages.error(request, 'Could not get access token.')
    else:
        error = True
        messages.error(request, 'You must have an oauth access code to login, '
                               'no code was provided.')

    if error:
        return HttpResponseRedirect(reverse('core:home'))
    else:
        return HttpResponseRedirect(reverse('core:pick'))


def oauth_logout(request):
    if request.session.get('access_token'):
        request.session['access_token'] = None

    messages.success(request, 'You have successfully logged out.')

    return HttpResponseRedirect(reverse('core:home'))
