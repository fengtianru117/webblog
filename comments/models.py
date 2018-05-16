from django.db import models


# Create your models here.

class Comment(models.Model):
    name = models.CharField('用户名', max_length=50)
    content = models.TextField('评论内容')
    create_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('blog.Article', on_delete=models.CASCADE, verbose_name='评论的父文章')

    def __str__(self):
        return self.content[:20]