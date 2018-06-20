from django.urls import re_path, path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^login/$', views.OAuthLoginView.as_view(), name='login'),
    re_path(r'^oauth/github/$',views.GitHubOAuthView.as_view(),name='github_oauth'),
]
