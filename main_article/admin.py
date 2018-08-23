from django.contrib import admin
from django.forms import ModelForm,TextInput
from suit.widgets import NumberInput,AutosizedTextarea,LinkedSelect,Select
from main_article.models import Article,Category,Userprofile,Contact,Daily_click,First_login
from django import forms

class ArticleForm(ModelForm):
    class Meta:
        
        widgets = {
            'title': TextInput(attrs={'class': 'input-xxlarge'}),
            'likes': NumberInput(attrs={'class': 'input-mini'}),
            'dislikes': NumberInput(attrs={'class': 'input-mini'}),
            'read_num': NumberInput(attrs={'class': 'input-mini'}),
            'comment_num': NumberInput(attrs={'class': 'input-mini'}),
            'excerpt': AutosizedTextarea(attrs={'rows': 3,'class': 'input-xlarge'})
            
            
        }
class ArticleModelAdmin(admin.ModelAdmin):
    form=ArticleForm
    list_display = ['id','title','read_num','likes','author','tag_list','pubDateTime','upDateTime']
    list_display_links = ['title']
    list_filter = ['title','pubDateTime','author']
    search_fields = ['title']
    class Meta:    
        model = Article     
    def get_queryset(self, request):
        return super(ArticleModelAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
        
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','pubDateTime']
    list_display_links = ['name']
    class Meta:
        model = Category
'''
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','pubDateTime']
    list_display_links = ['name']
    class Meta:
        model = Tag
'''        
'''
class UserProfileForm(ModelForm):
    class Meta:
        
        widgets = {
            'title': TextInput(attrs={'class': 'input-xxlarge'})            
        }
'''
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','get_articles','nickname','qq','address','weibourl','avatar','bonuspoints']
    list_display_links = ['user']
    
    def get_queryset(self, request):
        return admin.ModelAdmin.get_queryset(self, request).prefetch_related('user__user_articles')
    def get_articles(self,obj):     
        return u",".join(o.title for o in obj.user.user_articles.all()[:3])
    get_articles.short_description = '发表的文章'
    class Meta:
        model = Userprofile
    

class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id','from_user','to_user','created_time']
    list_display_links = ['from_user']
    class Meta:
        model = 'Contact'
class Daily_clickModelAdmin(admin.ModelAdmin):
    
    list_display = ['id','user','get_nickname','click_status','created_time']
    list_display_links = ['user']
    
    def get_nickname(self,obj):
        return obj.user.nickname
    get_nickname.short_description = '昵称'
    get_nickname.admin_order_field = '-user'    
    class Meta:
        model = 'Daily_click'
class First_loginModelAdmin(admin.ModelAdmin):
    
    list_display = ['id','user','first_login']
    list_display_links = ['user']  
    class Meta:
        model = 'First_login'
admin.site.register(Article,ArticleModelAdmin)
admin.site.register(Category,CategoryModelAdmin)
admin.site.register(Userprofile,UserProfileModelAdmin)
admin.site.register(Contact,ContactModelAdmin)
admin.site.register(Daily_click,Daily_clickModelAdmin)
admin.site.register(First_login,First_loginModelAdmin)

# Register your models here.