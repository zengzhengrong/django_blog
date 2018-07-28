from __future__ import absolute_import

import django
from django.urls import re_path
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from . import views

if django.VERSION >= (1, 8):
    urlpatterns = [
        re_path(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        re_path(r'^browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    ]
else:
    from django.conf.urls import patterns
    urlpatterns = patterns(
        '',
        url(r'^upload/', login_required(views.upload), name='ckeditor_upload'),
        url(r'^browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    )
