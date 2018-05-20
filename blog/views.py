import markdown
from django.shortcuts import render, get_object_or_404
from .models import Category, Article
from django.views.generic import ListView, DetailView
from comments.forms import CommentForm
from django.http import HttpResponse


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = super(IndexView, self).get_queryset().order_by('-publish_time')
        for a in article_list:
            a.content = markdown.markdown(a.content,
                                          extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                          ])
        return article_list


'''def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
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
    })'''


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, *kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        article = super(ArticleDetailView, self).get_object(queryset=None)
        article.content = markdown.markdown(article.content,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        return article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class CategoryView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('category_pk'))
        article_list = super(CategoryView, self).get_queryset().filter(category=cate).order_by('-publish_time')
        for a in article_list:
            a.content = markdown.markdown(a.content,
                                          extensions=[
                                              'markdown.extensions.extra',
                                              'markdown.extensions.codehilite',
                                              'markdown.extensions.toc',
                                          ])
        return article_list
