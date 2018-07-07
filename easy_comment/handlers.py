# coding=utf-8
from django.db.models.signals import post_save
from .models import Comment, Like
from notifications.signals import notify
from django.conf import settings
from django.apps import apps
from django.template.loader import render_to_string
from django.core.mail import send_mail
from extra_apps.django_private_chat.models import Dialog,Message
from main_article.models import Contact
import logging
logger = logging.getLogger('send_email')
def get_recipient():
    admins = [i[0] for i in settings.ADMINS]
    app_model = settings.AUTH_USER_MODEL.split('.')
    User_model = apps.get_model(*app_model) 
    recipient = User_model.objects.filter(username__in=admins)   
    return recipient

ADMINS = get_recipient()
SEND_NOTIFICATION_EMAIL = getattr(settings, 'SEND_NOTIFICATION_EMAIL', False)
def select_link(user,localhost='127.0.0.1:8000',host='pancake.red'):
    if settings.DEBUG == True:
        return '{}{}'.format(localhost,user.profile.get_notification_url())
    else:
        return '{}{}'.format(host,user.profile.get_notification_url())
def email_handler(*args):
    for user in args:
        try:
            if not (hasattr(user, 'onlinestatus') and user.onlinestatus.is_online()):
                context = {'receiver':user.username,
                           'unsend_count':user.notifications.filter(unread=True, emailed=False).count(),
                           'notice_list':user.notifications.filter(unread=True, emailed=False),
                           'unread_link':select_link(user) }
                msg_plain = render_to_string("notifications/email/email.html", context=context)
                send_mail("来自[Zzr的博客] 您有未读的评论通知",
                          msg_plain,
                          settings.EMAIL_HOST_USER,
                          recipient_list=[user.email])
                user.notifications.unsent().update(emailed=True)
        except Exception as e:
            print("Error in easy_comment.handlers.py.email_handler: %s" % e)

def comment_handler(sender, instance, created, **kwargs):
    if created:
        recipient = ADMINS.exclude(id=instance.user.id)
        if not instance.parent is None:
            recipient = recipient.exclude(id=instance.parent.user.id)#排除掉父类评论User是admin避免发送两次通知
            if recipient.count() > 0:#判断是否在settings.py中添加管理员
                notify.send(instance.user, recipient=recipient,
                            verb='回复了 %s' % instance.parent.user_name,
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)
                if SEND_NOTIFICATION_EMAIL:
                    logger.info('send_emalil_reply')
                    email_handler(*recipient)
            if not instance.user_name == instance.parent.user_name:
                notify.send(instance.user, recipient=instance.parent.user, verb='@了你',
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)
                if SEND_NOTIFICATION_EMAIL:
                    logger.info('send_emalil_@')
                    email_handler(instance.parent.user)
        else:
            if recipient.count() > 0:
                notify.send(instance.user, recipient=recipient, verb='发表了评论',
                            action_object=instance,
                            target=instance.post,
                            description=instance.content)
                if SEND_NOTIFICATION_EMAIL:
                    logger.info('send_emalil')
                    email_handler(*recipient)

post_save.connect(comment_handler, sender=Comment)

def like_handler(sender, instance, created, **kwargs):
    if created:
        recipient = ADMINS.exclude(id=instance.user.id).exclude(id=instance.comment.user.id)
        verb = '的评论' if instance.comment.parent is None else '的回复'
        action = '赞了' if instance.status else '踩了'
        if recipient.count() > 0:
            notify.send(instance.user, recipient=recipient,
                        verb=action+instance.comment.user_name+verb,
                        action_object=instance.comment,
                        target=instance.comment.post,
                        description=instance.comment.content)
        if (not instance.user.profile.nickname == instance.comment.user_name) and instance.status:
            notify.send(instance.user, recipient=instance.comment.user,
                        verb='赞了你'+verb,
                        action_object=instance.comment,
                        target=instance.comment.post,
                        description=instance.comment.content)

post_save.connect(like_handler, sender=Like)
'''
设置PM消息通知
'''
def chat_handler(sender, instance, created, **kwargs):  
    if created:
        print('working')
        notify.send(instance.owner,   
            recipient=instance.opponent,
            verb='和你创建聊天',
            description='')
        
post_save.connect(chat_handler, sender=Dialog) 


def message_handler(sender,instance,created,**kwargs):
    if created:
        print('success send notification')
        notify.send(instance.sender,
                    recipient=instance.dialog.opponent if not instance.dialog.opponent.username==instance.sender.username \
                    else instance.dialog.owner,
                    verb='私信了你',
                    description=instance.text)
post_save.connect(message_handler, sender=Message)


def follow_handler(sender,instance,created,**kwargs):
    if created:
        print('follow success')
        notify.send(instance.from_user.user,
                    recipient=instance.to_user.user,
                    verb='关注了你',
                    description=''
                    )
post_save.connect(follow_handler, sender=Contact)
    