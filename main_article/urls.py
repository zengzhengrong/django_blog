from django.conf.urls import url
from main_article import views
from main_article.views import RssFeed

urlpatterns = [
    #article
    url(r'^$',views.article,name = 'article'),
    url(r'^articleCreate/$', views.articleCreate, name='articleCreate'),
    url(r'^articleRead/(?P<articleId>[0-9]+)/$', views.articleRead, name='articleRead'),
    url(r'^articleUpdate/(?P<articleId>[0-9]+)/$', views.articleUpdate, name='articleUpdate'),
    url(r'^articleDelete/(?P<articleId>[0-9]+)/$', views.articleDelete, name='articleDelete'),
    url(r'^articleSearch/$', views.articleSearch, name='articleSearch'),
    url(r'^articleLike/(?P<articleId>[0-9]+)/$', views.articleLike, name='articleLike'), 
    url(r'^articleArchive/$', views.archive, name='articleArchive'),# archive
    #userlikes
    url(r'^superlikes/$', views.superlikes, name='superlikes'),
    #category
    url(r'^categoryControl/$', views.categoryControl, name='categoryControl'),
    url(r'^categoryRead/(?P<categoryId>[0-9]+)/$', views.categoryRead, name='categoryRead'),
    url(r'^categoryDelete/(?P<categoryId>[0-9]+)/$', views.categoryDelete, name='categoryDelete'),
    url(r'^categoryUpdate/(?P<categoryId>[0-9]+)/$', views.categoryUpdate, name='categoryUpdate'),

    #tag
    url(r'^tagControl/$', views.tagControl, name='tagControl'),
    url(r'^tagRead/(?P<tagId>[0-9]+)/$', views.tagRead, name='tagRead'),
    url(r'^tagDelete/(?P<tagId>[0-9]+)/$', views.tagDelete, name='tagDelete'),
    #user
    url(r'^userProfile/$', views.userProfile, name='userProfile'),
    url(r'^userList/$', views.user_list, name='userList'),
    url(r'^userRead/(?P<userId>[0-9]+)/$', views.userRead, name='userRead'),
    url(r'^userFollow/$', views.user_follow, name='user_follow'),
    url(r'^userFollowing/$', views.userFollowing, name='user_following'),
    url(r'^userFollowers/$', views.userFollowers, name='user_followers'),
    
    #Rss-feed
    url(r'^Rss/$', RssFeed(), name='Rss'),
    # DailyClick
    url(r'^dailyClick/$',views.User_Daily_Click, name='user_daily_click'),

    ] 