# coding=utf-8
from django import template
from main_article.models import Article,Category
from guestbook.models import Guestbook_Category
from taggit.models import Tag


register = template.Library()

@register.simple_tag
def get_all_category():
    category = Category.objects.all()
    return category
@register.simple_tag
def get_all_guestbook_category():
    guestbook_category = Guestbook_Category.objects.all()
    return guestbook_category
    
@register.simple_tag
def get_read_article():
    articles = Article.objects.all()
    read_numList = []
    read_maxList = []
    numList = []
    for article in articles:
        read_num = article.read_num
        read_numList.append(read_num)
        numList.append(read_num)
    set_numList = set(read_numList)
    set_read_numList = set(numList)
    sort_ready_list = sorted(list(set_numList&set_read_numList),reverse=True)    
    for i  in sort_ready_list:        
        article_read = Article.objects.filter(read_num = i)
        read_maxList.append(article_read)    
    return read_maxList[0:5]

@register.simple_tag
def get_all_tag():
    tagpost = Tag.objects.all()
    return tagpost

@register.simple_tag
def get_comment_article():
    commentpost = Article.objects.order_by('-comment_num')
    return commentpost[:5]

@register.simple_tag
def check_dialogs_messages(request):
    # 检查是否有创建对话框消息
    try:
        
        if request.user.selfDialogs.all() or request.user.toDialogs.all():
            # print(True)
            session = 'chat'
        else:
            # print(False)
            session = 'None_chat'
    except AttributeError:
        session = ''  
    return session
    
@register.simple_tag
def get_archives_all():
    articles_archive = Article.objects.all()
    return articles_archive

