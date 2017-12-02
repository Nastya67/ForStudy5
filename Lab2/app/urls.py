from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<arg>\d+and\d+)$', views.update, name='update'),
    url(r'^newGame$', views.insertGame, name='insertGame'),
    url(r'^newTime$', views.insertTime, name='insertTime'),
]