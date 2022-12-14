# ajapaik-mwapi
separate repository from Ajapaik-web for Wikimedia OAUTH and image uploading 

# Install
```
> git clone git@github.com:Ajapaik/ajapaik-mwapi.git
> cd ajapaik-mwapi
> python3 -m venv venv
> source venv/bin/activate
> venv/bin/python3 -m pip install --upgrade pip
> pip install -r requirements.txt
> cd src
> cp server/settings/local.example.py server/settings/local.py
```
## Edit local configuration to server/settings/local.py 
* USE_BETA_COMMONS defines if we are using Wikimedia production or [Beta-cluster](https://commons.wikimedia.beta.wmflabs.org). Use Beta for developing.  
* SECRET_KEY value is long random string
* CSRF_TRUSTED_ORIGINS and ALLOWED_HOSTS should match to your hostname if it is other than localhost
* SOCIAL_AUTH* = Oauth1 consumer settings. See [My first Django OAuth tool](https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Django_OAuth_tool) for more info.

#### Register OAUTH1 consumer 
* Wikimedia: https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose 
* Wikimedia Beta-Cluster: https://meta.wikimedia.beta.wmflabs.org/wiki/meta:Special:OAuthConsumerRegistration/propose

To request changes to the software configuration, the creation of new Beta Cluster wikis or user rights, please file a task in Phabricator.
If you are doing more testing then you can request Oauth approval rights to beta cluster for yourself.
* https://phabricator.wikimedia.org/maniphest/task/create/?projects=Beta-Cluster


#### Oauth consumer proposal checklist
* Oauth version: OAuth 1.0a consumer
* Application name: use a name that indicates that you are developing locally
* Leave "This consumer is for use only by <your username>" unchecked
* Contact email address: Use a valid email where you can be reached.
* Applicable project: All is fine
* OAuth "callback" URL: http://127.0.0.1:8000/
* Select: Allow consumer to specify a callback in requests and use "callback" URL above as a required prefix.
* Types of grants being requested: (for uploading photos)
.* Edit existing pages
.* Create, edit, and move pages
.* Upload new files
.* Upload, replace, and move files
* Public RSA key: You can leave this empty at the moment.


## Run migrations 
```
> python manage.py makemigrations webservice
> python manage.py migrate

## Start test server
> python manage.py runserver 8000
```
Open https://127.0.0.1:8000/ with browser and do OAUTH login.

### Port forwarding
Making server visible on the public internet. Example only (command needs to be edited to get it working)

```
> sudo -u username ssh -N -L 8000:127.0.0.1:8000 username@server.org -i /home/username/.ssh/id_rsa
```


# Management commands

This will show users logged in
* [src/server/management/commands/userinfo.py](https://github.com/Ajapaik/ajapaik-mwapi/blob/main/src/server/management/commands/userinfo.py)
```
> python manage.py userinfo 
```
This will upload one random image from Wikimedia Commons to Beta Commons
* [src/server/management/commands/uploadtest.py](https://github.com/Ajapaik/ajapaik-mwapi/blob/main/src/server/management/commands/uploadtest.py)
```
> python manage.py uploadtest  
```


# Reseting the database
```
> rm src/server/db.sqlite3
> rm -rf src/webservice/migrations/*
> python manage.py makemigrations webservice
> python manage.py migrate
```
  
# URLS
* https://127.0.0.1:8000/
* https://127.0.0.1:8000/profile
* https://127.0.0.1:8000/upload
* https://127.0.0.1:8000/accounts/login
* https://127.0.0.1:8000/logout
* https://127.0.0.1:8000/accounts/launcher/ (Flutter App magic link)

## REST API
* https://127.0.0.1:8000/api/profile
* https://127.0.0.1:8000/api/upload
* https://127.0.0.1:8000/api/logout

