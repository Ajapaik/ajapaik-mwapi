from server.settings.default import *

DEBUG = True

USE_BETA_COMMONS = True
SOCIAL_AUTH_MEDIAWIKI_KEY = ''
SOCIAL_AUTH_MEDIAWIKI_SECRET = ''
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://commons.wikimedia.beta.wmflabs.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'https://ajapaik.ee/oauth/complete/mediawiki'

CSRF_TRUSTED_ORIGINS = ['https://ajapaik.ee','https://*.127.0.0.1']
ALLOWED_HOSTS = ['ajapaik.ee', 'localhost', '127.0.0.1']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#92s+2$0u0c^_lmequj27ep^lryo6a!(98jqf-%jxkl(-1frcl'
