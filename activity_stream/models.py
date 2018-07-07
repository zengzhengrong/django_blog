from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(User,related_name='actions',db_index=True,verbose_name='动作发出者')
    verb = models.CharField(max_length=100,verbose_name='动作描述')
    action_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='ct_action',verbose_name='动作类型')
    ct_id = models.PositiveIntegerField(null=True,blank=True,db_index=True,verbose_name='动作类型ID')
    action = GenericForeignKey('action_ct','ct_id')
    created = models.DateTimeField(auto_now_add=True,db_index=True,verbose_name='建立时间')
    class Meta():
        ordering = ('-created',)
        verbose_name='用户动作'
        verbose_name_plural=verbose_name
    def get_ct_name(self):
        return str(self.action_ct)
        
        
# Create your models here.
