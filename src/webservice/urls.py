from django.urls import path, include
from webservice import views,api

urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('accounts/login', views.login_oauth, name='login'),
    path('upload', views.upload_file, name='upload'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('accounts/launcher/', views.oauthdone, name='oauthdone'),
    path('', views.index),

    path('api/logout', api.api_logout.as_view(), name='api.logout'),
    path('api/profile', api.api_profile.as_view(), name='api.profile'),
    path('api/upload', api.api_upload_file.as_view(), name='api.upload')
]
