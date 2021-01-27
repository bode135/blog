from django.shortcuts import render
# 导入数据模型ArticlePost
from .models import ArticlePost
# def article_list(request):
#     # 取出所有博客文章
#     articles = ArticlePost.objects.all()
#     # 需要传递给模板（templates）的对象
#     context = {'articles': articles}
#     # render函数：载入模板，并返回context对象
#     return render(request, 'article/list.html', context)

# 引入分页模块
from django.core.paginator import Paginator
import markdown
from comment.models import Comment

# def article_list(request):
#     # 修改变量名称（articles -> article_list）
#     article_list = ArticlePost.objects.all()
#
#     # 每页显示 1 篇文章
#     paginator = Paginator(article_list, 6)
#     # 获取 url 中的页码
#     page = request.GET.get('page')
#     # 将导航对象相应的页码内容返回给 articles
#     articles = paginator.get_page(page)
#
#     context = {'articles': articles}
#     return render(request, 'article/list.html', context)

# # 重写文章列表
# def article_list(request):
#     # 根据GET请求中查询条件
#     # 返回不同排序的对象数组
#     if request.GET.get('order') == 'total_views':
#         article_list = ArticlePost.objects.all().order_by('-total_views')
#         order = 'total_views'
#     else:
#         article_list = ArticlePost.objects.all()
#         order = 'normal'
#
#     # Question: 这里每次都把所有文章取出来, 然后再做分页, 不会读写速度太慢么?
#     paginator = Paginator(article_list, 3)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#
#     # 修改此行
#     context = { 'articles': articles, 'order': order }
#
#     return render(request, 'article/list.html', context)


# 引入 Q 对象
from django.db.models import Q



def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()


    paginator = Paginator(article_list, 4)      # 每页文章数
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # get_article_abstract
    if(1):
        def get_article_abstract(article):
            html = markdown.markdown(article.body)
            content = etree.HTML(html)
            pure_text = content.xpath('string()')  # 减去 链接 | 图片 | 资源 后的 纯文本.

            import re
            reg = re.compile(r'<.*?>')  # 去掉标签
            pure_text = reg.sub('', pure_text)

            reg = re.compile(r'`{3}.*`{3}', re.S)  # 去掉标签
            pure_text = reg.sub('<**代码块**>', pure_text)

            # reg = re.compile(r'\n', re.S)  # 加入换行失败, 以后研究.
            # pure_text = reg.sub('<br>', pure_text)

            # print(pure_text[:100])

            # pure_text = markdown.markdown(pure_text)
            abstract = pure_text
            return abstract

        from lxml import etree
        for article in articles:

            article.abstract = get_article_abstract(article)

    # 增加 search 到 context
    context = { 'articles': articles, 'order': order, 'search': search }
    return render(request, 'article/list.html', context)

# 文章详情
# def article_detail(request, id):
#     # 取出相应的文章
#     article = ArticlePost.objects.get(id=id)
#     # 需要传递给模板的对象
#     context = { 'article': article }
#     # 载入模板，并返回context对象
#     return render(request, 'article/detail.html', context)

# ------------ markdown

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',

                                         # 目录扩展
                                         'markdown.extensions.toc',
                                     ]
                                     )

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # context = { 'article': article }
    # 添加comments上下文
    context = {'article': article, 'comments': comments}

    # 修改 Markdown 语法渲染
    # md = markdown.Markdown(
    #     extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         'markdown.extensions.toc',
    #     ]
    # )
    # article.body = md.convert(article.body)

    # 新增了md.toc对象
    # context = {'article': article, 'toc': md.toc}

    return render(request, 'article/detail.html', context)


# -------------- forms

# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=1)

            print('---------------- new_article.title: ', new_article.title)
            print('---------------- new_article.href: ', new_article.href)

            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = { 'article_post_form': article_post_form }
        # 返回模板
        return render(request, 'article/create.html', context)

# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")

# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
# 提醒用户登录
from django.contrib.auth.decorators import login_required
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article, 'article_post_form': article_post_form }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


from django.views.generic.edit import CreateView

class ArticleCreateView(CreateView):
    model = ArticlePost

    fields = '__all__'
    # 或者只填写部分字段，比如：
    # fields = ['title', 'content']

    # article/create_by_class_view
    template_name = 'article/create_by_class_view.html'


# <editor-fold desc='类视图'>

# from django.views import View
#
# class ArticleListView(View):
#     """处理GET请求"""
#     def get(self, request):
#         articles = ArticlePost.objects.all()
#         context = {'articles': articles}
#         return render(request, 'article/list.html', context)
#

from django.views.generic import ListView

class ArticleListView(ListView):
    # 上下文的名称
    context_object_name = 'articles'
    # 查询集
    queryset = ArticlePost.objects.all()
    # 模板位置
    template_name = 'article/list.html'

article_list_example = ArticleListView.as_view()
# article_list = ArticleListView.as_view()
# </editor-fold>


# from django.views.generic import DetailView
#
# class ArticleDetailView(DetailView):
#     queryset = ArticlePost.objects.all()
#     context_object_name = 'article'
#     template_name = 'article/detail.html'