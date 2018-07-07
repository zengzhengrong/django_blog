from django.contrib import admin
from guestbook.models import Guestbook_Post,Guestbook_Category


class Guestbook_PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','read_num','author','tag_list','pubDateTime','upDateTime']
    list_display_links = ['title']
    list_filter = ['title','pubDateTime','author']
    search_fields = ['title']
    class Meta:    
        model = Guestbook_Post     
    def get_queryset(self, request):
        return super(Guestbook_PostModelAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all()) 
class Guestbook_CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','pubDateTime']
    list_display_links = ['name']
    class Meta:
        model = Guestbook_Category
admin.site.register(Guestbook_Post,Guestbook_PostModelAdmin)
admin.site.register(Guestbook_Category,Guestbook_CategoryModelAdmin)

# Register your models here.
