from django.views.generic import TemplateView, View
from django.conf import settings  # 等同于 from fengtianru117 import settings
import requests
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import redirect
from django.contrib.auth import login

class OAuthLoginView(TemplateView):
    '第三方登录视图'
    template_name = 'account/login.html'

    def get_context_data(self, **kwargs):
        context = super(self, OAuthLoginView).get_context_data()
        if 'next' in self.request.GET:
            # next为转到登录页面之前用户正在浏览的页面
            # 保存到session里以便登录完成后跳转回之前的页面
            self.request.session['next'] = self.reuqest.GET['next']
            context['github_oauth_url'] = \
                'https://github.com/login/oauth/authorize?client_id={}' \
                    .format(settings.GITHUB_CLIENT_ID)
        return context


class OAuthView(View):
    '具体的实现比如微博 github 在其他类里面，其他类可以继承这个类'
    # 这个类视图应写的尽量通用，关于GitHub的用户认证逻辑应放在子类中实现
    # 这样日后想要使用其他第三方登录方式时，只需继承这个类
    # 再补充一点逻辑即可，无需重写所有代码

    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def get(self, request, *args, **kwargs):
        # 可以把get方法看成对视图的简单调用
        access_token = self.get_access_token(request)
        user_info = self.get_user_info(access_token)

    def get_access_token(self, request):
        '获取access token'
        url = self.access_token_url
        # 在请求头里申明接受json格式的返回数据
        headers = {'Accept': 'application/json'}
        # 构造data
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': request.GET['code']
        }
        # 发送请求到access_token_url
        r = requests.post(url, data, headers=headers, timeout=1)
        # 解析返回的json数据
        result = r.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            # 由于code是临时的用户标记
            # 如果code过期了，则无法得到access_token
            # 这种情况下应该抛出禁止访问的错误，django会返回403
            raise PermissionDenied

    def get_success_url(self):
        '获取登录成功后返回的页面'
        if 'next' in self.request.session:
            # next保存了用户登录前正在浏览的网站
            # 比如当用户想要评论某篇文章时需要登录
            # 这时next就应保存那篇文章的url
            # 等用户完成登录操作后，依然可以继续他的评论，而不是跳到其他网页去了
            return self.request.session.pop('next')
        else:
            # 没有就返回主页
            return '/'

class GitHubOAuthView(OAuthView):
    'github账号认证视图'
    # 在具体类当中构造相应的参数
    access_token_url='https://github.com/login/oauth/access_token'
    user_api = 'https://api.github.com/user?access_token='
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET

    def authenticate(self, user_info):
        '用户认证'
        user = User.objects.filter(profile__github_id=user_info['id'])
        # 在数据库中检索GitHub id
        # 如果有，则选择相应的用户登录
        # 如果没有，则创建用户，然后再登录
        if not user:
            # 用户的模型见下文
            # user_info里'login'为用户名，'id'为GitHub的id，'avatar_url'为用户头像的url
            # 除此还有很多其他信息，如果想知道，直接print(user_info)
            user = User.objects.create_user(user_info['login'])
            profile = Profile(
                user=user,
                github_id=user_info['id'],
                avatar=user_info['avatar_url'])
            profile.save()
        else:
            user = user[0]
        # 用login函数登录，logout函数注销
        login(self.request, user)
        return redirect(self.get_success_url())