# -*- coding: utf-8 -*-
from django.urls import re_path

from extra_apps.django_private_chat import views

urlpatterns = [
    re_path(
        r'^dialogs/(?P<username>[\w.@+-]+)$',
        view=views.DialogListView.as_view(),
        name='dialogs_detail'
    ),
    re_path(
        r'^dialogs/$',
        view=views.DialogListView.as_view(),
        name='dialogs'
    ),
]
