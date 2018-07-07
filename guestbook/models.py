from django.db import models
from django.contrib.auth.models import User
from extra_apps.ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
from taggit.managers import TaggableManager
from time import timezone
from django.core.urlresolvers import reverse


class Guestbook_Category(models.Model):
    name = models.CharField(max_length=12,unique=True,blank=False)
    pubDateTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-pubDateTime']
        verbose_name='留言板分类'
        verbose_name_plural=verbose_name

class Guestbook_Post(models.Model):
    category = models.ForeignKey(Guestbook_Category,verbose_name='分类')
    tags = TaggableManager(help_text='(选填)用英文输入法逗号来分割标签',blank=True)
    title = models.CharField(max_length=128, unique=True,verbose_name='标题')
    content = RichTextUploadingField(verbose_name='正文',config_name='guestbook')
    pubDateTime = models.DateTimeField(auto_now_add=True,verbose_name='发表时间')
    upDateTime = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    read_num = models.IntegerField(default=0,verbose_name='阅读次数')
    author = models.ForeignKey(User,verbose_name='作者')
    comment_num = models.IntegerField(default=0,verbose_name='评论数') 
    class Meta:
        ordering = ['-pubDateTime']
        verbose_name='留言板文章'
        verbose_name_plural=verbose_name
    #摘录
    '''
    def save(self,*args, **kwargs):
        if not self.excerpt:
            self.excerpt = strip_tags(self.content)[:200]  
        super(Guestbook_Post,self).save(*args, **kwargs)
    '''
    
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('guestbook:postRead',args=[self.id])
# Create your models here.
