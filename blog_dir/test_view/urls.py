# 引入path
from django.urls import path
from . import views
from django.views.generic.base import RedirectView

# 正在部署的应用的名称
app_name = 'test_view'

urlpatterns = [
    path('', RedirectView.as_view(url='author_list/')),

    # path('article_list_example/', views.article_list_example, name='article_list_example'),

    # http://127.0.0.1:8000/test_view/contact_view
    path('contact_view/', views.ContactView.as_view(), name='contact_view'),
    # http://127.0.0.1:8000/test_view/author_create
    # path('author_create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author_create/', views.author_create, name='author_create'),
    path('author_list/', views.author_list, name='author_list'),

    # http://127.0.0.1:8000/test_view/thanks
    path('thanks/', views.thanks, name='thanks'),
    # path('thanks/', views.thanks, name='thanks'),
    # path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
]