import time
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny
from webservice.mediawiki import check_and_upload_file_to_commons, get_wikimediacommons_url
from webservice import forms

# Response statuses
RESPONSE_STATUSES = {
    'OK': 0,  # no error
    'UNKNOWN_ERROR': 1,  # unknown error
    'INVALID_PARAMETERS': 2,  # invalid input parameter
    'MISSING_PARAMETERS': 3,  # missing input parameter
    'ACCESS_DENIED': 4,  # access denied
    'SESSION_REQUIRED': 5,  # session is required
    'SESSION_EXPIRED': 6,  # session is expired
    'INVALID_SESSION': 7,  # session is invalid
    'USER_ALREADY_EXISTS': 8,  # user exists in the DB already
    'INVALID_APP_VERSION': 9,  # application version is not supported
    'MISSING_USER': 10,  # user does not exist
    'INVALID_PASSWORD': 11,  # wrong password for existing user
}

# Disable Csrf so that it is easier to make curl and flutter queries
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class AjapaikAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def _handle_request(self, data, user, request):
        return Response({
            'error': RESPONSE_STATUSES['INVALID_PARAMETERS'],
            'photos': []
        })
    def post(self, request, format=None):
        return self._handle_request(post, request.user, request)

    def get(self, request, format=None):
        return self._handle_request(request.GET, request.user, request)

class api_upload_file(AjapaikAPIView):
    def post(self, request, format=None):
        ret=check_and_upload_file_to_commons(request)

        if ret:
            return Response({
                'error': RESPONSE_STATUSES['OK'],
                'messages':ret
            })
        else:
            return Response({
                'error': RESPONSE_STATUSES['INVALID_PARAMETERS'],
            })

class api_profile(AjapaikAPIView):
    def _handle_request(self, data, user, request):
        content = {
            'error': 0,
            'state': str(int(round(time.time() * 1000)))
        }

        if user.is_authenticated:
            content['name'] = str(user)
        return Response(content)

class api_logout(AjapaikAPIView):
    def _handle_request(self, data, user, request):
        errorcode = 0 if user.is_authenticated else 2
        logout(request)
        return Response({'error': errorcode})
