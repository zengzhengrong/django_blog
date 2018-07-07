from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment, Like
# Register your models here.

class CommentAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ['user','post','parent','content','submit_date']
    list_filter = ['post','submit_date','user']
    search_fields = ['user']
    #list_editable = ['content']
    #sortable = 'submit_date'
    class Meta:
        model = Comment 

admin.site.register(Comment,CommentAdmin)
admin.site.register(Like)

