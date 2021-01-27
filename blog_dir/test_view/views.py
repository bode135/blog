from django.shortcuts import render, redirect

# Create your views here.
from test_view.forms import ContactForm
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'test_view/contact.html'
    form_class = ContactForm
    # success_url = 'test_view/posted.html'
    success_url = 'test_view/thanks'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

from django.http import HttpResponse
def thanks(request):
    return HttpResponse("谢谢使用.")


# from django.views import View
# class AuthorCreate(View):
#     """处理GET请求"""
#     def get(self, request):
#         # articles = ContactForm.objects.all()
#         # context = {'articles': articles}
#         template_name = 'test_view/create_author.html'
#         # form_class = ContactForm
#         # context = {'author_name': author_name}
#         # return render(request, 'article/list.html', context)
#         return render(request, template_name, form_class)
#
#     def post(self, request):
#         from test_view.models import Author
#
#         # articles = ContactForm.objects.all()
#         # context = {'articles': articles}
#
#         model = Author
#         fields = ['name']
#
#         # return render(request, 'test_view/posted.html', context)
#         return  redirect("test_view:thanks")

from .forms import CreateAuthorForm
def author_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # return HttpResponse("under developing................")
        # article_post_form = CreateAuthorForm(data=request.POST)


        # 将提交的数据赋值到表单实例中
        create_author_form = CreateAuthorForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if create_author_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            # new_author = create_author_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            # new_author.author = User.objects.get(id=1)
            new_author = create_author_form.save(commit=False)
            # new_author.name = request.POST['title']
            # create_author_form.save()
            # print('---------------- new_author.name: ', new_author.name)

            # 将新文章保存到数据库中
            new_author.save()
            # 完成后返回到文章列表
            return redirect("test_view:thanks")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        create_author_form = CreateAuthorForm()
        # 赋值上下文
        context = {'name': create_author_form}
        # 返回模板
        return render(request, 'test_view/create.html', context)

def author_list(request):
    from .models import AuthorPost
    authors_list = AuthorPost.objects.all()
    authors = authors_list

    context = {'authors': authors}
    return render(request, 'test_view/list.html', context)

# from django.views.generic.edit import CreateView
# from test_view.models import Author
#
# #
# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['name']
#
#     success_url = '../thanks'
#     # success_url = 'test_view/thanks'