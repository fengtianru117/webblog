from django.conf.urls import re_path
from . import views

app_name = 'testrsa'
urlpatterns = [
    re_path(r'^testrsa$', views.testrsa, name='testrsa'),
    re_path(r'^encrypt$', views.encrypt, name='encrypt'),
]
