import markdown
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Article
from .models import Category
from django.views.generic import ListView

# Create your views here.
from django.http import HttpResponse
from .models import Article

'''
def index(request):
    # article_list = Article.objects.get(pk=2)
    article_list = Article.objects.all().order_by('-publish_time')
    for a in article_list:
        a.content = markdown.markdown(a.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])

    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })
'''


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        # article_list = super(IndexView,self).get_queryset().order_by('-publish_time')
        article_list = Article.objects.all().order_by('-publish_time')
        for a in article_list:
            a.content = markdown.markdown(a.content,
                                          extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                          ])
        return article_list


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                        ])
    return render(request, 'blog/detail.html', context={
        'article': article
    })


def category(request):
    # c = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.all().order_by('-publish_time')
    for a in article_list:
        a.content = markdown.markdown(a.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
    return render(request, 'blog/article_list.html', context={
        'article_list': article_list
    })
