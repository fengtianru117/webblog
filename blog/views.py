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
    paginate_by = 6

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

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

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


class CategoryView(IndexView):
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
