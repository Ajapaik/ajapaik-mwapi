from social_django.models import UserSocialAuth, Nonce, Association
from requests_oauthlib import OAuth1Session
from oauthlib.oauth2 import TokenExpiredError
import json
from server.settings import SOCIAL_AUTH_MEDIAWIKI_KEY,SOCIAL_AUTH_MEDIAWIKI_SECRET, USE_BETA_COMMONS

def get_wikimediacommons_url():
    if USE_BETA_COMMONS:
	    return "https://commons.wikimedia.beta.wmflabs.org"
    else:
	    return "https://commons.wikimedia.org"

def get_userinfo_url():
    return get_wikimediacommons_url() + '/w/api.php?format=json&action=query&meta=userinfo&uiprop=blockinfo%7Cgroups%7Crights%7Chasmsg'

def get_mediawiki_client(user_id):
    usersocialauth = UserSocialAuth.objects.filter(provider='mediawiki',user_id=1).first()

    if not usersocialauth:
        print("UserSocialAuth not found")
        return False

    print(str(usersocialauth.provider))
    oauth_token=usersocialauth.extra_data.get('access_token').get('oauth_token')
    oauth_token_secret=usersocialauth.extra_data.get('access_token').get('oauth_token_secret')

    try:
        client = OAuth1Session(
                     SOCIAL_AUTH_MEDIAWIKI_KEY, 
                     client_secret=SOCIAL_AUTH_MEDIAWIKI_SECRET,
                     resource_owner_key=oauth_token,
                     resource_owner_secret=oauth_token_secret)

    except TokenExpiredError as e:
        print("TokenExpireError")
        return False

    return client

def get_csrf_token(client):
    edit_token_url = get_wikimediacommons_url() + '/w/api.php?action=query&meta=tokens&format=json'
    r = client.get(edit_token_url)
    data=r.json()
    csrf_token=data['query']['tokens']['csrftoken']
    return csrf_token


def get_mediawiki_whoami(client):
    if client:
       r = client.get(get_userinfo_url())
       return r
    else:
       return False

def upload_file_to_commons(client, source_filename, target_filename, wikitext, comment):
    mediawiki_api_url=get_wikimediacommons_url() + "/w/api.php"
    csrf_token=get_csrf_token(client)
    upload_payload={
        'action': 'upload',
        'format':'json',
        'filename':target_filename,
        'comment':comment,
        'text':wikitext,
        'ignorewarnings': 1,
        'token':csrf_token,
    }
    files={'file': (target_filename, open(source_filename,'rb'),'multipart/form-data')}
    r = client.post(mediawiki_api_url, data=upload_payload, files=files)
    return r

def check_and_upload_file_to_commons(request):
    form = forms.UploadFileForm(request.POST, request.FILES)
    if not form.is_valid():
        return False

    user_id=request.user.id
    source_filename=request.FILES['file'].temporary_file_path()
    target_filename=form.cleaned_data['title']
    wikitext=form.cleaned_data['wikitext']
    uploaded_file_url=get_wikimediacommons_url() + '/wiki/File:' +target_filename +'.jpeg'
    
    client=get_mediawiki_client(user_id)
    if not client:
        return False

    if not source_filename:
        return False

    if not target_filename:
        return False

    if not wikitext:
        return False

    comment="Uploading self photographed test file to Commons. CC-BY"
    ret= upload_file_to_commons(client, source_filename, target_filename, wikitext, comment)
    return ret
