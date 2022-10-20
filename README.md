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
#Edit local configuration to server/settings/local.py (see registering Oauth1 consumer)
> python manage.py makemigrations webservice
> python manage.py migrate
```

#Register OAUTH1 consumer 
* Wikimedia LIVE: https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose 
* Wikimedia Beta: https://meta.wikimedia.beta.wmflabs.org/wiki/meta:Special:OAuthConsumerRegistration/propose

To request changes to the software configuration, the creation of new Beta Cluster wikis or user rights, please file a task in Phabricator.
If you are doing more testing then you can request Oauth approval rights to beta cluster for yourself.
* https://phabricator.wikimedia.org/maniphest/task/create/?projects=Beta-Cluster

## Oauth consumer proposal checklist
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

# For reseting the database
> rm src/server/db.sqlite3
> rm -rf src/webservice/migrations/*
> python manage.py makemigrations webservice
> python manage.py migrate


