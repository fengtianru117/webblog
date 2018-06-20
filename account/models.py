from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    '用户资料'
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='account/avatar', max_length=200, null=True, blank=True, verbose_name='头像')
    github_id = models.PositiveIntegerField('GitHub id', unique=True, null=True, blank=True)
