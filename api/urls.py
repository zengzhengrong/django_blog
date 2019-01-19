from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import re_path
from . import views
api_urlpatterns = format_suffix_patterns([
    re_path(r'^api/$', views.api_root,name='api-index'),
    re_path(r'^api/article-list/$', views.ArticleList.as_view(),name='article-list'),
    re_path(r'^api/article/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(),name='article-detail'),
])