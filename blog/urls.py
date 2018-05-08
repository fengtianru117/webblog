from django.conf.urls import re_path
from . import views

app_name = 'blog'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^article/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^article/category/$', views.category, name='category'),
    # re_path(r'^categories/$', views.category, name='category'),
]
