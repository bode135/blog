# 引入path
from django.urls import path
from . import views
from django.views.generic import RedirectView


# 正在部署的应用的名称
app_name = 'article'


urlpatterns = [
    path('', RedirectView.as_view(url='article-list/')),

    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # 安全删除文章
    path(
        'article-safe-delete/<int:id>/',
        views.article_safe_delete,
        name='article_safe_delete'
    ),
    # 更新文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),

    path('create-view/', views.ArticleCreateView.as_view(), name='ArticleCreateView'),
    # path('article_list_example/', views.ArticleListView.as_view(), name='article_list_example'),
    path('article_list_example/', views.article_list_example, name='article_list_example'),


    # path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
]