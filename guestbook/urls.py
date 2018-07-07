from django.conf.urls import url
from guestbook import views


urlpatterns = [
    #CRUDS
    url(r'^posts/$', views.guestbook_index,name='posts'),
    url(r'^postRead/(?P<postId>[0-9]+)/$', views.guestbook_Post_Read, name='postRead'),
    url(r'^posts/PostCreate/$', views.guestbook_Post_Create,name='postCreate'),  
    url(r'^postUpdate/(?P<postId>[0-9]+)/$', views.guestbook_Post_Update, name='postUpdate'),
    url(r'^postDelete/(?P<postId>[0-9]+)/$', views.guestbook_Post_Delete, name='postDelete'),
    #guestbook_category
    url(r'^g_categoryRead/(?P<g_categoryId>[0-9]+)/$', views.g_categoryRead, name='g_categoryRead'),
    url(r'^g_categoryDelete/(?P<g_categoryId>[0-9]+)/$', views.g_categoryDelete, name='g_categoryDelete'),
    url(r'^g_categoryUpdate/(?P<g_categoryId>[0-9]+)/$', views.g_categoryUpdate, name='g_categoryUpdate'),
    ]

