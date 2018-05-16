import markdown
from django.shortcuts import render, get_object_or_404
from .models import Category, Article
from django.views.generic import ListView, DetailView
from comments.forms import CommentForm
from django.http import HttpResponse

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


'''def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        article_list = Article.objects.all().order_by('-publish_time')
        for a in article_list:
            a.content = markdown.markdown(a.content,
                                          extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                          ])
        context['article_list'] = article_list
        return context'''


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc',
                                        ])
    form = CommentForm()
    comment_list = article.comment_set.all()
    return render(request, 'blog/detail.html', context={
        'article': article,
        'form': form,
        'comment_list': comment_list,
    })


def category(request, category_pk):
    # cate = get_object_or_404(Category,pk=category_pk)
    cate = Category.objects.get(pk=category_pk)
    article_list = Article.objects.filter(category=cate).order_by('-publish_time')
    for a in article_list:
        a.content = markdown.markdown(a.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
    return render(request, 'blog/article_list.html', context={
        'article_list': article_list,
    })
