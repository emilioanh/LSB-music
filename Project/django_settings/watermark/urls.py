from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.home, name='homepage'),
    path(r'signup', views.signup, name='signup'),
    path(r'buy/<song_id>', views.buy, name='buy'),
    path(r'upload', views.upload, name='upload'),
    path(r'mysong', views.mysong, name='mysong'),
    path(r'decode', views.decode, name='decode'),
]