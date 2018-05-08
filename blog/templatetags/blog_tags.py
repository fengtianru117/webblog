from django import template
from ..models import Article, Category

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-publish_time')[:num]


@register.simple_tag
def get_article_categories():
    return Category.objects.filter(pk__gte=1)


'''
@register.simple_tag
def get_article_category_names():
    return Category.objects.all()
'''