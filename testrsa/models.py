from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class PrivateKey(models.Model):
    n = models.TextField('n')
    e = models.TextField('e')
    d = models.TextField('d')
    p = models.TextField('p')
    q = models.TextField('q')
