from django.conf.urls import re_path
from . import views
from django.views.static import serve
from django.conf import settings

app_name = 'blog'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^article/(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    re_path(r'^article/category/(?P<category_pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    # re_path(r'^categories/$', views.category, name='category'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
