from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from webservice.forms import UploadFileForm, OauthDoneForm
from webservice.mediawiki import check_and_upload_file_to_commons, get_wikimediacommons_url


# Create your views here.
def index(request):
    context = {}
    return render(request, 'web/index.dtl', context)

@login_required()
def profile(request):
    context = {'commons_server_url':get_wikimediacommons_url()}
    return render(request, 'web/profile.dtl', context)

def login_oauth(request):
    context = {}
    return render(request, 'web/login.dtl', context)

def logout_view(request):
    context = {}
    logout(request)
    return render(request, 'web/index.dtl', context)

# Uploads file to Wikimedia Commons
def upload_file(request):
    if request.method == 'POST':
        ret=check_and_upload_file_to_commons(request)
        if ret:
            return render(request, 'web/profile.dtl', {'form': form, 'upload_status':'OK', 'uploaded_file_url':uploaded_file})
        else:
            return render(request, 'web/profile.dtl', {'form': form, 'upload_status':'ERROR 2'})
    else:
        form = UploadFileForm()
        return render(request, 'web/profile.dtl', {'form': form, 'upload_status':'ERROR 1'})

# Renders html page which redirects user to link 
# ajapaik://ajapaik.ee/accounts/launcher?route=$route&provider=$provider&token=$token

def oauthdone(request):
    user = request.user
    form = OauthDoneForm(request.GET)
    if form.is_valid():
        if user.is_anonymous:
            return HttpResponse('No user found', status=404)

        provider=form.cleaned_data['provider']
        allowed_providers=[ 'mediawiki']
        if provider not in allowed_providers:
            return HttpResponse('Provider not in allowed providers.' + provider, status=404)

        usersocialauth = UserSocialAuth.objects.filter(provider='mediawiki', user_id=user.id).first()
        if not usersocialauth:
            return HttpResponse('Token not found.', status=404)

        token=usersocialauth.extra_data.get('access_token').get('oauth_token')
        context = {
            'route': '/login',
            'provider': provider,
            'token': token
        }
        return render(request, 'web/oauthdone.dtl', context)

    return HttpResponse('No user found', status=404)
