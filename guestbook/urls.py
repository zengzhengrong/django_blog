from django.urls import re_path
from guestbook import views


urlpatterns = [
    #CRUDS
    re_path(r'^posts/$', views.guestbook_index,name='posts'),
    re_path(r'^postRead/(?P<postId>[0-9]+)/$', views.guestbook_Post_Read, name='postRead'),
    re_path(r'^posts/PostCreate/$', views.guestbook_Post_Create,name='postCreate'),  
    re_path(r'^postUpdate/(?P<postId>[0-9]+)/$', views.guestbook_Post_Update, name='postUpdate'),
    re_path(r'^postDelete/(?P<postId>[0-9]+)/$', views.guestbook_Post_Delete, name='postDelete'),
    #guestbook_category
    re_path(r'^g_categoryRead/(?P<g_categoryId>[0-9]+)/$', views.g_categoryRead, name='g_categoryRead'),
    re_path(r'^g_categoryDelete/(?P<g_categoryId>[0-9]+)/$', views.g_categoryDelete, name='g_categoryDelete'),
    re_path(r'^g_categoryUpdate/(?P<g_categoryId>[0-9]+)/$', views.g_categoryUpdate, name='g_categoryUpdate'),
    ]

