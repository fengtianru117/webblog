from django.conf.urls import re_path
from . import views

app_name = 'comments'
urlpatterns = [
    re_path(r'^comment/post/(?P<article_pk>[0-9]+)/$', views.article_comment, name='article_comment'),
]
