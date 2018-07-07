"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
import notifications.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', include('main_article.urls',namespace='main_article')),
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^.*', include('main_article.urls')),#与ckeditor图片预览冲突
    url(r'^', include('main_article.urls')), 
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'', include('easy_comment.urls')),
    url(r'^notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^guestbook/',include('guestbook.urls', namespace='guestbook')),
    url(r'^', include('extra_apps.django_private_chat.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


