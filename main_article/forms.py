from django import forms
from main_article.models import Article,Category,Userprofile,THUMB_TYPE_CHOICES
from extra_apps.ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User
from taggit.models import Tag
from allauth.account.adapter import DefaultAccountAdapter
import re
#from ckeditor.widgets import CKEditorWidget
#from ckeditor_uploader.widgets import CKEditorUploadingWidget





class ArticleForm(forms.ModelForm):
    title = forms.CharField(label='标题',max_length=128,widget=forms.TextInput(attrs={'class':'form-group','placeholder':'必填'}))   
    content = forms.CharField(label='正文',widget = CKEditorUploadingWidget())
    category = forms.ModelChoiceField(label='分类',queryset=Category.objects.all())
    thumb_type = forms.ChoiceField(label='生成封面类型',choices=THUMB_TYPE_CHOICES,widget=forms.Select(attrs={'onchange':'show_thumb()'}))
    thumbnail = forms.ImageField(label='自定义封面',required=False,widget=forms.FileInput(attrs={'class':'form-group hidden'})) 
    #tags = forms.CharField(label='标签(选填)',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用空格或者英文逗号分割标签'}))

    class Meta:
        model = Article
        fields = ('title','category','thumb_type','thumbnail','tags','content')
    
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

class ChangePasswordForm(forms.Form):
    original_password = forms.CharField(label='原密码',
                                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'输入原密码','type':'password'}))
    new_password = forms.CharField(label='新密码',
                                        max_length=10,
                                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'输入新密码(6-10个字符)','type':'password'}))
    new_password_again = forms.CharField(label='再次输入新密码',
                                         max_length=10,
                                         widget=forms.TextInput(attrs={'class':'form-control','placeholder':'输入新密码(6-10个字符)','type':'password'}))
    ##在forms添加request,判断用户是否在线
    def __init__(self,*args,**kwargs):
        # 重新初始化
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm,self).__init__(*args,**kwargs)
    def clean(self):
        original_password = self.cleaned_data.get('original_password','').strip()
        new_password = self.cleaned_data.get('new_password','')   
        new_password_again = self.cleaned_data.get('new_password','')
        # 检测原密码有效性
        if not self.user.check_password(original_password):
            raise forms.ValidationError(('原密码不正确'),code='invalid')
        # 原密码和新密码不能一样
        if original_password == new_password:
            raise forms.ValidationError(('原密码和新密码不能一样'),code='invalid')
        # 检测新密码一致性
        if new_password != new_password_again:
            raise forms.ValidationError(('两次输入新密码不一致'),code='invalid')
        # 密码不为空
        if new_password =='':
            raise forms.ValidationError(('新密码不能为空'),code='invalid')
        # 检验密码长度
        if len(new_password) < 6:
            raise forms.ValidationError(('密码太短（6-10字符）'),code='invalid')
        return self.cleaned_data

class ChangeEmailForm(forms.Form):
    original_email = forms.EmailField(label='原邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'输入原邮箱地址'}))
    email = forms.EmailField(label='新邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'输入新邮箱地址'}))
    verification_code = forms.CharField(label='验证码',
                                        required=False,
                                        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'输入验证码'}))
    
    ##在forms添加request,判断用户是否在线
    def __init__(self,*args,**kwargs):
        # 重新初始化
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeEmailForm,self).__init__(*args,**kwargs)
    
        
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code','').strip()
        if verification_code == '':
            raise forms.ValidationError(('验证码不能为空'),code='null')
            
        if not verification_code.isdigit():
            raise forms.ValidationError(('格式不对'),code='invalid')
            
        return verification_code
    def clean(self):
        # 判断用户是否登陆
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError(('用户没有登陆'),code='invalid_user')
        # 验证邮箱有效性
        email = self.cleaned_data.get('email').strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('你要绑定的邮箱已经被绑定')
        
        # 判断验证码
        code = self.request.session.get('%s_change_email' % self.request.user.username)
        verification_code = self.cleaned_data.get('verification_code','').strip()
        # print(code)
        # print(verification_code)
        if (code=='' or code != verification_code):
            raise forms.ValidationError(('验证码不正确'),code='invalid_verification_code')
        
        return email
    
    
    
    
            