from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('分类', max_length=100)

    def __str__(self):
        return self.name

    '''
    class Meta:
        verbose_name='分类'
        verbose_name_plural='分类'
    '''


class Tag(models.Model):
    name = models.CharField('标签', max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    # 文章
    title = models.CharField('标题', max_length=70)
    cover = models.ImageField(upload_to='blog/cover', verbose_name='封面图', null=True, blank=True)  # 路径问题回头再试一试
    content = models.TextField('内容')
    publish_time = models.DateTimeField('发布日期')
    # 作者与分类的默认值为2和1,代表着相应数据库中id的字段,分别手动将其设置为了fengtianru117和未分类
    author = models.ForeignKey(User, default=2, on_delete=models.SET_DEFAULT, verbose_name='作者')
    category = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT, verbose_name='分类')
    tag = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='标签')

    # views =

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
