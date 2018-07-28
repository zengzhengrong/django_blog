# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from extra_apps.ckeditor_uploader.fields import RichTextUploadingField
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.utils.html import strip_tags
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils import timezone
import urllib.parse
import codecs
import sys

#


#User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))    



class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, blank=True, null=True, verbose_name='昵称')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    weibourl = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人微博地址')
    address = models.CharField(max_length=128, blank=True,null=True,verbose_name='地址')
    following = models.ManyToManyField('self',through='Contact',blank=True,related_name='followers',symmetrical=False)
    bonuspoints = models.PositiveIntegerField(default=0,verbose_name='饼果')  
    avatar = ProcessedImageField(upload_to='avatar',
                                 default='avatar/default.png', 
                                 verbose_name='头像',
                                 processors=[ResizeToFill(85,85)],
                                 )  
    class Meta:
        verbose_name='个人信息'
        verbose_name_plural=verbose_name
    def get_absolute_url(self):
        return reverse('main_article:userRead',args=[self.id])  
    def get_notification_url(self):
        return reverse('notifications:all')
    def __str__(self):
        return self.user.username 
    #复写save()方法
    def save(self, *args, **kwargs):
        # 原来的存取方式'avatar'/'avatar.name'
        # 修改为'avatar'/'user.username'/'avatar.name'
        # 将self.avatar.name加入到序列中，判断元素是否唯一
        # self.avatar.name = [self.avatar.name]
        #print(self.avatar.name.split('/'))
        if len(self.avatar.name.split('/')) == 1:
            self.avatar.name = '%s/%s' % (self.user.username,self.avatar.name)
            self.avatar.name = urllib.parse.quote(self.avatar.name)[:10]
            # print(self.avatar.name)
        super(Userprofile, self).save()

    def get_nickname_or_username(self): # 获取nickname或者username
        if Userprofile.objects.filter(user=self.user).exists():
            profile = Userprofile.objects.get(user=self.user)
            if self.nickname == '' or self.nickname == None:
                return self.user.username
            else:
                return self.nickname
        else:
            return self.user.username
        
class First_login(models.Model):
    user = models.OneToOneField(User, related_name='user_first_login',on_delete=models.CASCADE)
    first_login = models.BooleanField(default=True,verbose_name=u'第一次登陆')
    
    class Meta:
        verbose_name='首登'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.user.username 
    
        
class Contact(models.Model):
    from_user = models.ForeignKey(Userprofile,related_name='user_from',verbose_name='用户',on_delete=models.CASCADE)
    to_user = models.ForeignKey(Userprofile,related_name='user_to',verbose_name='关注',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta:
        ordering = ['-created_time']
        verbose_name='关注'
        verbose_name_plural=verbose_name
    def __str__(self):
        return '{} 关注  {}'.format(self.from_user, self.to_user)
        
class Category(models.Model):
    name = models.CharField(max_length=12,unique=True,blank=False)
    pubDateTime = models.DateTimeField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse('main_article:categoryRead',args=[self.id])
    class Meta:
        ordering = ['-pubDateTime']
        verbose_name='文章分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class Daily_click(models.Model):
    user = models.ForeignKey(Userprofile,related_name='user_click',verbose_name='签到用户',unique=False,on_delete=models.CASCADE)
    click_status = models.NullBooleanField(verbose_name='签到状态')
    created_time = models.DateTimeField(default=timezone.now,verbose_name='签到时间')    
    class Meta:
        verbose_name='每日签到'
        verbose_name_plural=verbose_name
        ordering = ['-created_time']
    def __str__(self):
        return self.user.user.username

class Article(models.Model):
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.SET_NULL,null=True)
    tags = TaggableManager(help_text='(选填)用英文输入法逗号来添加标签',blank=True,verbose_name='标签集')
    title = models.CharField(max_length=128, unique=True,verbose_name='标题')
    content = RichTextUploadingField(verbose_name='正文')
    likes = models.IntegerField(default=0,verbose_name='赞')
    dislikes = models.IntegerField(default=0,verbose_name='踩')
    pubDateTime = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    upDateTime = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    read_num = models.IntegerField(default=0,verbose_name='阅读次数')
    author = models.ForeignKey(User,verbose_name='作者',related_name='user_articles',on_delete=models.SET_NULL,null=True)
    comment_num = models.IntegerField(default=0,verbose_name='评论数') 
    excerpt = models.CharField(max_length=200, blank=True,verbose_name='摘录') 
    superlikes = models.ManyToManyField(User,blank=True,verbose_name='超级赞',related_name='user_likes')
    class Meta:
        ordering = ['-pubDateTime']
        verbose_name='文章'
        verbose_name_plural=verbose_name
    def save(self,*args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.content)[:200]  
        super(Article,self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('main_article:articleRead',args=[self.id])
    def __str__(self):
        return self.title
    
      

   
# Create your models here.
