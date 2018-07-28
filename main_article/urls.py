from django.urls import re_path
from main_article import views
from main_article.views import RssFeed

urlpatterns = [
    #article
    re_path(r'^$',views.article,name = 'article'),
    re_path(r'^articleCreate/$', views.articleCreate, name='articleCreate'),
    re_path(r'^articleRead/(?P<articleId>[0-9]+)/$', views.articleRead, name='articleRead'),
    re_path(r'^articleUpdate/(?P<articleId>[0-9]+)/$', views.articleUpdate, name='articleUpdate'),
    re_path(r'^articleDelete/(?P<articleId>[0-9]+)/$', views.articleDelete, name='articleDelete'),
    re_path(r'^articleSearch/$', views.articleSearch, name='articleSearch'),
    re_path(r'^articleLike/(?P<articleId>[0-9]+)/$', views.articleLike, name='articleLike'), 
    re_path(r'^articleArchive/$', views.archive, name='articleArchive'),# archive
    #userlikes
    re_path(r'^superlikes/$', views.superlikes, name='superlikes'),
    #category
    re_path(r'^categoryControl/$', views.categoryControl, name='categoryControl'),
    re_path(r'^categoryRead/(?P<categoryId>[0-9]+)/$', views.categoryRead, name='categoryRead'),
    re_path(r'^categoryDelete/(?P<categoryId>[0-9]+)/$', views.categoryDelete, name='categoryDelete'),
    re_path(r'^categoryUpdate/(?P<categoryId>[0-9]+)/$', views.categoryUpdate, name='categoryUpdate'),

    #tag
    re_path(r'^tagControl/$', views.tagControl, name='tagControl'),
    re_path(r'^tagRead/(?P<tagId>[0-9]+)/$', views.tagRead, name='tagRead'),
    re_path(r'^tagDelete/(?P<tagId>[0-9]+)/$', views.tagDelete, name='tagDelete'),
    #user
    re_path(r'^userProfile/$', views.userProfile, name='userProfile'),
    re_path(r'^userList/$', views.user_list, name='userList'),
    re_path(r'^userRead/(?P<userId>[0-9]+)/$', views.userRead, name='userRead'),
    re_path(r'^userFollow/$', views.user_follow, name='user_follow'),
    re_path(r'^userFollowing/$', views.userFollowing, name='user_following'),
    re_path(r'^userFollowers/$', views.userFollowers, name='user_followers'),
    
    #Rss-feed
    re_path(r'^Rss/$', RssFeed(), name='Rss'),
    # DailyClick
    re_path(r'^dailyClick/$',views.User_Daily_Click, name='user_daily_click'),
    # SecurityCenter
    re_path(r'^change_email/$',views.changeemail, name='changeemail'),
    re_path(r'^change_password/$',views.changepassword, name='changepassword'),
    re_path(r'^send_email_code/$',views.send_email_code, name='send_email_code'),
    
    ] 