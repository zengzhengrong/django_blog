from django import forms
from main_article.models import Article,Category,Userprofile
from extra_apps.ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User
from taggit.models import Tag
from allauth.account.adapter import DefaultAccountAdapter
import re
#from ckeditor.widgets import CKEditorWidget
#from ckeditor_uploader.widgets import CKEditorUploadingWidget





class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='标题',max_length=128)   
    content = forms.CharField(label='正文',widget = CKEditorUploadingWidget())
    category = forms.ModelChoiceField(label='分类',queryset=Category.objects.all()) 
    #tags = forms.ModelMultipleChoiceField(label='标签(选填)',queryset=Tag.objects.all(),widget=forms.CheckboxSelectMultiple(attrs={'class': 'nav nav-tabs navbar-default img-rounded'}),required=False)

    class Meta:
        model = Article
        fields = ('title','tags','content','category')
    
    def clean(self):
        cleanedData = self.cleaned_data
        title = cleanedData.get('title')
        content = cleanedData.get('content')
        bans = ('shit','bitch','caonima','fuck','Fuck')
        '''
        replace_str = '***'        
        print(title)
        print(content)
        '''
        for ban in bans:
            # If title and content were not find ban word return cleanedData
            # The find funtion is not find ban word will output -1
            if title.find(ban)==-1 and content.find(ban)==-1:
                pass
            else:              
                #new_title = title.replace(ban,replace_str,title.count(ban))
                #print(title)
                #print(new_title)               
                #title = new_title
                #print(title)
                #return cleanedData
                raise forms.ValidationError(('标题或正文含有违禁词'+'(' + ban + ')'),code = 'invalid')
        return cleanedData
        '''
            except ValueError:
                return cleanedData
        '''
        '''
        print(title)
        content = cleanedData.get('content')
        if title!=content:
            raise forms.ValidationError('标题和内容不相符')
        return cleanedData
        '''
        
class UserprofileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('avatar','nickname','qq','weibourl','address')
        
'''
在allauth下新增验证：
1，username不允许使用中文
2.password不能全是数字
'''
class Myadapter(DefaultAccountAdapter):
    
    def clean_username(self, username, shallow=False):
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        username = str(username)                  
        result = zh_pattern.search(username)
        if result:
            raise forms.ValidationError(('用户名不能为中文'),code = 'invalid')

        return DefaultAccountAdapter.clean_username(self, username, shallow=shallow)
    def clean_password(self, password, user=None):
        if password.isdigit():
            raise forms.ValidationError(('密码不能全为数字'),code = 'invalid')
        
        return DefaultAccountAdapter.clean_password(self, password, user=user)
