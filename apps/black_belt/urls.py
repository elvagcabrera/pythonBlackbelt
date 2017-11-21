from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^process$', views.process),
    url(r'^favorite$', views.favorite),
    url(r'^removeFavorite$', views.removeFavorite),
    url(r'^viewUser/(?P<id>\d+)$', views.viewUser),
]