from django.contrib import admin
from activity_stream.models import Action


class Actionadmin(admin.ModelAdmin):
    list_display = ('user','verb','action','created')
    list_filter = ('created',)
    search_fuelds = ('verb',)

admin.site.register(Action,Actionadmin)

# Register your models here.
