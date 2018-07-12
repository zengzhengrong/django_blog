# coding=utf-8
import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from main_article.models import Article,Category,Userprofile,Contact,Daily_click,First_login
from easy_comment.models import Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from main_article.forms import ArticleForm,UserprofileForm
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from taggit.models import Tag
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decorators.decorator import admin_required,ajax_required,author_required
from django.utils.html import strip_tags
from django.http.response import HttpResponse
from activity_stream.utils import create_action
from activity_stream.models import Action
from guestbook.models import Guestbook_Category
from multiprocessing.sharedctypes import template
from django.views.decorators.cache import cache_page
from .utils import save_avatar_img
import logging
logger = logging.getLogger('main_article')


def Check_Daily_Click(request):
    now = timezone.now()
    # 取日期和时间，来确定时间轴
    hours = timezone.now().hour
    minutes = timezone.now().minute
    seconds = timezone.now().second
    microseconds = timezone.now().microsecond
    timedelte = now - datetime.timedelta(hours=hours,minutes=minutes,seconds=seconds,microseconds=microseconds)
    # ORM 过滤在此时间轴的user签到
    # 判断是否登录
    try:
        sanme_clicked_ojs = Daily_click.objects.filter(created_time__gt=timedelte,user=request.user.profile)
        if not sanme_clicked_ojs :
            # 管理员自动签到
            if request.user.is_superuser:
                create_click_oj = Daily_click(user=request.user.profile,click_status=True,created_time=timezone.now())
                create_click_oj.save()
            return False
    except AttributeError:
        pass
    return True

def article(request): 
    # print(Article.objects.values('id','title'))
    if request.user.is_active:
        First_login.objects.get_or_create(user=request.user)
        if request.user.user_first_login.first_login == True:
            print(u'first_login')              
            try:
                # print(hasattr(request.user.socialaccount_set.first(), 'get_avatar_url'))
                if hasattr(request.user.socialaccount_set.first(), 'get_avatar_url'):
                    print(u'Third party account... Create user information')                
                    github_avatar_url = request.user.socialaccount_set.first().get_avatar_url()
                    get_avatar_path=save_avatar_img(github_avatar_url,file_name=request.user.username)
                    # print(get_avatar_path)
                    Userprofile.objects.get_or_create(user=request.user,avatar=get_avatar_path)
                    first_login_alter = get_object_or_404(First_login, user=request.user)
                    first_login_alter.first_login = False
                    first_login_alter.save()
                    print(u'end')
                else:
                    print(u'No third party account... Create user information')
                    Userprofile.objects.get_or_create(user=request.user)
                    first_login_alter = get_object_or_404(First_login, user=request.user)
                    first_login_alter.first_login = False
                    first_login_alter.save()
                    print(u'end')
            except Exception as e:
                print (u'error：',e)   
        pass
    articles = Article.objects.all()
    for article in articles:
        
        
        commentnum = Comment.objects.filter(post = article)
        article.comment_num = commentnum.__len__()        
        article.save()

    # 上述为文章显示和阅读量显示
    articlecount = articles.__len__()
         
    paginator = Paginator(articles,4)
    # print(dir(paginator))
    page_num = request.GET.get('page',1)

    try:
        articles = paginator.page(page_num)
        current_page = articles.number # 获取当前页面num
        current_page_round = list(range(max(current_page-2,1),current_page))+\
        list(range(current_page,min(current_page+2,paginator.num_pages)+1))
        # print(current_page_round)       
        # print(current_page)
        # 添加省略号
        if current_page_round[0]-1 >= 2:
            current_page_round.insert(0,'...')
        if current_page_round[-1]-paginator.num_pages <= -2:
            current_page_round.append('...')
        # 添加首页尾页
        if current_page_round[0] != 1 :
            current_page_round.insert(0,1)
        if current_page_round[-1] != paginator.num_pages :
            current_page_round.append(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    # 上述为文章分页功能
    # 获取站长信息
    '''
    superuser = User.objects.get(username='admin')
    master = get_object_or_404(Userprofile,user=superuser)
    '''
    master = User.objects.get(username='admin')
    context = {'articles':articles,
               'current_page_round':current_page_round,
               'articlecount':articlecount,
               'master':master
               }
    
    '''
    if request.user.is_active:
        #print(request.user)
        user = get_object_or_404(User,username=request.user)
        if user.last_login == user.date_joined:
            print('创建用户信息。。。')
            Userprofile.objects.get_or_create(user=user) 
            print('成功')
        else:
            # 由日期格式函数转换称字符串格式函数用strftime()
            # 由字符串格式转换成日期格式的函数用strptime()
            strdatetime_last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
            print(strdatetime_last_login)
            strdatetime_joined = user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            print(strdatetime_joined)
            if strdatetime_last_login == strdatetime_joined:
                print(True)
            print('fail')
    '''
    # 每日签到
    
    if Check_Daily_Click(request):
        context['clickstuts']='已签到'
    else:
        context['clickstuts']='签到'
            
         
    return render(request, 'main_article/index.html',context)
@admin_required
@login_required
def articleCreate(request):
    template = 'main_article/articlecreateupdate.html'
    if request.method == 'GET':       
        return render(request, template,{'articleForm':ArticleForm(),'tags':Tag.objects.all()})

    # POST
    articleForm = ArticleForm(request.POST)
    
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})
    # 从页面获取user信息
    author_id = request.user  
    articleform = articleForm.save(commit=False)    
    articleform.author = author_id
    articleform.upDateTime = timezone.now()
    articleform.save()
    articleForm.save_m2m()
    '''
            动作描述
    '''
    create_action(request.user, '发表了文章', articleform)
    # add tags 
    
    '''
    tag_name =Tag.objects.get(id=request.POST.get('tag'))
    article_title = request.POST.get('title')
    article_add_tag = Article.objects.get(title = article_title)
    article_add_tag.tag.add(tag_name)
    article_add_tag.save()
    '''
    
    
    messages.success(request,'文章已新增')
    return redirect('main_article:article')


    
def articleRead(request,articleId):
    
    if request.method == 'GET':
        template = 'main_article/articleRead.html'
        articleToRead = get_object_or_404(Article, id=articleId)
        
        logger.info(articleToRead)
        if not request.COOKIES.get('blog_%s_read_num' % articleId):
            # print('read+1')
            articleToRead.read_num += 1
            articleToRead.save()
        
        # print()
        # print(Comment.objects.filter(post=articleToRead).__len__())
    
    # print(articleToRead.tags.all())
    similar_article = articleToRead.tags.similar_objects()
    # print(similar_article)
    # print(articleToRead.superlikes.count())
 
    context = {
    'article': articleToRead,
    'comment_num':Comment.objects.filter(post=articleToRead).__len__(),
    'similar_articles':similar_article[:5],
    'superlikes':articleToRead.superlikes.all()[:5],
    
    }
    
    '''
    #上下文章之方法一
    article_all_list = []
    post = Article.objects.all()
    print(post[0])
    print(Article.objects.all()[0])
    for post in post:
        article_all_list.append(post.id)
    print(article_all_list)
    if article_all_list.index(articleToRead.id)==0:
        previous_post = '没有上一篇'
        next_post = Article.objects.all()[1]
    elif article_all_list.index(articleToRead.id)==article_all_list.__len__()-1:
        previous_post = Article.objects.all()[article_all_list.__len__()-2]
        next_post = '没有下一篇'
    else:
        previous_post = Article.objects.all()[article_all_list.index(articleToRead.id)-1]
        next_post = Article.objects.all()[article_all_list.index(articleToRead.id)+1]
    '''
    
    # 方法二
    previous_post = Article.objects.filter(pubDateTime__gt=articleToRead.pubDateTime).last()
    next_post = Article.objects.filter(pubDateTime__lt=articleToRead.pubDateTime).first()
    if previous_post==None:
        previous_post = '没有了'
    if next_post==None:
        next_post = '没有了'
    context['previous_article'] = previous_post
    context['next_article'] = next_post
    response = render(request, template , context)
    response.set_cookie('blog_%s_read_num' % articleId, 'have_read',max_age=120)
    return response
    
    

@login_required
def articleUpdate(request, articleId):
    articleToUpdate = get_object_or_404( Article, id=articleId)
    template = 'main_article/articlecreateupdate.html'
    #print(articleToUpdate.author)
    
    if request.method == 'GET':  
        if not request.user == articleToUpdate.author:
            messages.error(request, '你没有权限')
            return redirect('main_article:article')

        articleForm = ArticleForm(instance=articleToUpdate)
        return render(request, template, {'articleForm':articleForm, 'article':articleToUpdate,'tags':Tag.objects.all()})
    # POST
    articleForm = ArticleForm(request.POST, instance=articleToUpdate)

    # print(articleForm)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm, 'article':articleToUpdate})
    
    articleUpdateForm = articleForm.save(commit=False)
    
    articleUpdateForm.upDateTime = timezone.now()
    articleUpdateForm.excerpt = strip_tags(articleUpdateForm.content)[:200]
    articleUpdateForm.save()
    articleForm.save_m2m()
    create_action(request.user, '修改了文章',articleUpdateForm)
    messages.success(request, '文章已修改')
    return redirect('main_article:articleRead', articleId=articleId)
def articleDelete(request, articleId):
    
    if request.method == 'GET':
        return article(request)
    
    # POST
    articleToDelete = get_object_or_404(Article, id=articleId)
    articleToDelete_str = str(articleToDelete)
    articleToDelete.delete()
    create_action(request.user, '删除了文章'+'-'+articleToDelete_str, articleToDelete)
    messages.success(request, '文章已刪除')
    return redirect('main_article:article')
def articleSearch(request):
    searchTerm = request.GET.get('searchTerm')
    articles = Article.objects.filter(Q(title__icontains=searchTerm) |
                                      Q(content__icontains=searchTerm))
    context = {'articles':articles,
               'searchTerm' : searchTerm,
               'article_num':articles.__len__()}
    return render(request, 'main_article/articleSearch.html', context)
def articleLike(request,articleId):
    template = 'main_article/articleRead.html'
    articleToRead = get_object_or_404(Article, id=articleId)
    articleToRead.likes += 1
    articleToRead.save()
    # return redirect('main_article:articleRead', articleId=articleId)
    '''
            若采用上述回访形式的话，点赞会重新访问articleRead的url，导致阅读量也会加1
            采用下面只回复范本，url没有变。但是按刷新按钮时点赞会自动加1.
    '''
    context = {
        'article': articleToRead,
        'comment_num': Comment.objects.filter(post=articleToRead).__len__()
                }
    return render(request, template, context)
@login_required
def categoryControl(request):
    template = 'main_article/categoryControl.html'
    category = Category.objects.all()
    guestbook_category = Guestbook_Category.objects.all()
    if request.method =='GET':       
        context = {'categorys':category,'guestbook_categorys':guestbook_category,'articlecount':category.__len__()}
        return render(request, template,context)
    # POST
    content = request.POST.get('content')
    guestbook_content = request.POST.get('guestbook_content')
    # print('主页分类:'+str(content))
    # print('留言分类:'+str(guestbook_content))
    if content == '' or guestbook_content == '':
        context = {'categorys':category,'guestbook_categorys':guestbook_category,'articlecount':category.__len__()}
        messages.error(request, '不能为空')
        return render(request, template,context)   
    try:
        if not content == None:
            #print(content)
            content2=str(Category.objects.get(name=content))
            if content2==content:
                messages.error(request, '已存在')
        
    except Category.DoesNotExist:   
        categoryform = Category()
        categoryform.name = content
        categoryform.save()
        
        create_action(request.user, '添加了分类',categoryform)  
        messages.success(request, '新增成功')
    # 留言分类
    try:
        if not guestbook_content == None:
            #print(guestbook_content)
            content2_guestbook = str(Guestbook_Category.objects.get(name=guestbook_content))
            if content2_guestbook==guestbook_content:
                messages.error(request, '已存在')
    except Guestbook_Category.DoesNotExist:      
        guestbook_category_form = Guestbook_Category()
        guestbook_category_form.name = guestbook_content
        guestbook_category_form.save()
        
        messages.success(request, '新增成功')
                
        
    
    return redirect('main_article:categoryControl')

def categoryRead(request,categoryId):
    template = 'main_article/index.html'
    articles = Article.objects.filter(category=categoryId)
    
    '''
    由于计算文章留言function在article程式里，所以要调用一下，已达到在url为categoryRead页面显示评论数。
    不需要在点击article链接
    '''
    articlecount = articles.__len__()
    paginator = Paginator(articles,4)
    page_num = request.GET.get('page',1)
    try:
        articles = paginator.page(page_num)
        current_page = articles.number # 获取当前页面num
        current_page_round = list(range(max(current_page-2,1),current_page))+\
        list(range(current_page,min(current_page+2,paginator.num_pages)+1))
        # 添加省略号
        if current_page_round[0]-1 >= 2:
            current_page_round.insert(0,'...')
        if current_page_round[-1]-paginator.num_pages <= -2:
            current_page_round.append('...')
        # 添加首页尾页
        if current_page_round[0] != 1 :
            current_page_round.insert(0,1)
        if current_page_round[-1] != paginator.num_pages :
            current_page_round.append(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {'articles':articles, 
               'current_page_round':current_page_round,           
               'articlecount':articlecount
               }
    return render(request, template,context)
@login_required
def categoryDelete(request,categoryId):
    # POST
    category = get_object_or_404(Category,id=categoryId)
    category_str = str(category)
    category.delete()
    create_action(request.user, '删除了分类'+'-'+category_str,category)
    messages.success(request, '板块已删除')
    
    return redirect('main_article:categoryControl')
@login_required
def categoryUpdate(request,categoryId):
    template = 'main_article/categoryUpdate.html'
    category = get_object_or_404(Category,id=categoryId)
    if request.method == 'GET':
        return render(request, template,{'category':category})
    # POST
    content = request.POST.get('content')
    category.name = content
    category.save()
    create_action(request.user, '修改了分类',category)
    # print(content)
    messages.success(request,'板块已修改')
    return redirect('main_article:categoryControl')
def tagRead(request,tagId):
    template = 'main_article/index.html'
    articles = Article.objects.filter(tags=tagId)
    '''
    由于计算文章留言function在article程式里，所以要调用一下，已达到在url为categoryRead页面显示评论数。
    不需要在点击article链接
    '''
    articlecount = articles.__len__()
    paginator = Paginator(articles,4)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
        
    context = {'articles':articles,
               'articlecount':articlecount

               }
    return render(request, template,context)

def tagControl(request):
    template = 'main_article/tagControl.html'
    tags = Tag.objects.all()
    content = request.POST.get('content')
    if request.method == 'GET':
        context ={'tags':tags,
                  'articlecount':tags.__len__()
                    }
        return render(request, template, context)
    #post
    if content=='':
        context = {'tags':tags}
        messages.error(request, '不能为空')
        return render(request, template,context) 
    try:
        content2=str(Tag.objects.get(name=content))
        if content2==content:
            messages.error(request, '已存在')
    except Tag.DoesNotExist:   
        tagform = Tag()
        tagform.name = content
        tagform.save()
        create_action(request.user, '添加了标签',tagform)  
        messages.success(request, '新增成功')  
    return redirect('main_article:tagControl')

def tagDelete(request,tagId):
    tag_delete = Tag.objects.get(id=tagId)
    tag_delete_str = str(Tag.objects.get(id=tagId))
    tag_delete.delete()
    create_action(request.user, '删除了标签'+'-'+tag_delete_str,tag_delete)
    messages.success(request, '已删除:'+tag_delete_str)
    return redirect('main_article:tagControl')

def userProfile(request):
    '''
    UserProfile setting
    '''
    # user_to_read = Userprofile.objects.get(id=userId)
    # user = User.objects.get(username=request.user)
    user_to_read = Userprofile.objects.get(user=request.user)  
    template = 'main_article/UserProfile.html'
    if request.method == 'GET':
        user_articles = Article.objects.filter(author=request.user)
        user_comments = Comment.objects._mptt_filter(user=request.user).order_by('-submit_date')
        profileupdateform = UserprofileForm(instance=user_to_read)
        user_articles_count = user_articles.count()
        #右侧栏显示我发布的文章
        myposts = Article.objects.filter(author=request.user).order_by('-read_num')
        #显示用户动态
        #actions = Action.objects.filter(user=request.user)
        ##优化 加载速度提高50ms
        actions = Action.objects.filter(user=request.user).select_related('user','user__profile').prefetch_related('action')
        '''获取ct的obj类名来判断，满足不同的转址需求
        for action in actions:
            print(action.get_ct_name())
        '''
        '''
        pagination
        '''
        paginator_articles = Paginator(user_articles,10)
        #paginator_comments = Paginator(user_comments,5)
        page = request.GET.get('page')
        #print(user_articles.count()),采用分页设计，将无法使用.count()方法,需要重新生成对象
        try:
            user_articles = paginator_articles.page(page)
            #user_comments = paginator_comments.page(page)
        except PageNotAnInteger:
            user_articles = paginator_articles.page(1)
            #user_comments = paginator_comments.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            #user_comments = paginator_comments(paginator_comments.num_pages)
        
        context = {
            'userprofileform':profileupdateform,
           'userRead':user_to_read,
           'user_articles':user_articles,
           'user_comments':user_comments,
           'user_articles_count':user_articles_count,
           'userprofile':'userprofile',
           'myposts':myposts[0:5],
           'myactions':actions[0:10]
           }
        
        if request.is_ajax():
            template_list = 'main_article/user_articles_list_ajax.html'         
            return render(request,template_list,{'user_articles':user_articles})
        return render(request,template,context)
    #post
    #profileupdate = Userprofile.objects.get(user=userId)
    profileform = UserprofileForm(request.POST,request.FILES,instance=user_to_read)
    if not profileform.is_valid():
        return render(request, template, {'userprofileform':profileform,'userRead':user_to_read})
    
    profile = profileform.save(commit=False)  
    profile.save() 
    create_action(request.user, '修改了用户信息',profile)
    messages.success(request, '修改成功')
    
    return redirect('main_article:userProfile')
@admin_required
@login_required
def user_list(request):
    template = 'main_article/UserList.html'
    users = Userprofile.objects.exclude(user=request.user)
    context = {'session':'user_list','users':users}
    return render(request, template, context)
    


def userRead(request,userId):
    user_to_read = Userprofile.objects.get(id=userId)
    #print(user_to_read.followers.all())
    user_articles = Article.objects.filter(author=user_to_read.user)
    user_comments = Comment.objects._mptt_filter(user=user_to_read.user).order_by('-submit_date')
    user_articles_count = user_articles.count()
    #print(user_articles)
    actions = Action.objects.filter(user=userId).select_related('user','user__profile').prefetch_related('action')
   
    #print(user_articles.count())
    #print(user_articles_count)
    '''
    for user_comment in user_comments:        
        print(user_comment.user)
        print(user_comment.post)
        print(user_comment.content)
    #print(user_articles.count())
    '''
    
    #pagination
    
    paginator_articles = Paginator(user_articles,10)        
    page = request.GET.get('page')
    try:
        user_articles = paginator_articles.page(page)       
    except PageNotAnInteger:
        user_articles = paginator_articles.page(1)       
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        
  
    if request.is_ajax():
        template_list = 'main_article/user_articles_list_ajax.html'
        context = {
            'user_articles':user_articles
            }         
        return render(request,template_list,context)
    
    template = 'main_article/userRead.html'
    context = {'userRead':user_to_read,
               'user_articles':user_articles,
               'user_comments':user_comments,
               'user_articles_count':user_articles_count,
               'actions':actions[0:10]}
    return render(request, template,context)

def userFollowing(request):
    template = 'main_article/userFollowing.html'
    myFollowings = Contact.objects.filter(from_user=request.user.profile).select_related('to_user', 'to_user__user').prefetch_related('to_user__user__actions')
    '''
    for following in myFollowings:
        print(following.to_user)
        print(following.to_user.user.actions.all())  
    '''  
    
    return render(request,template,{'myFollowings':myFollowings})
    
def userFollowers(request):
    template = 'main_article/UserList.html'
    userfans = Userprofile.objects.get(user=request.user)
    #.select_related('user').prefetch_related('followers')
    '''
    for userfan in userfans:
        print(userfan.followers.all())
    '''
    context ={'userfans':userfans,
              'session':'fans'}
    return render(request, template, context)

@ajax_required
@login_required
@require_POST
def superlikes(request):
    #异步刷新(AJAX)
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = Article.objects.get(id=article_id)
            if action == 'like':
                article.superlikes.add(request.user)
                create_action(request.user, '点赞',article)
            else:
                article.superlikes.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})
    '''
    #同步刷新
    print(request.user)
    user = User.objects.get(username=request.user)
    article_to_like = Article.objects.get(id=articleId)
    article_to_like.likes +=1
    article_to_like.superlikes.add(user) 
    article_to_like.save()
    return redirect('main_article:articleRead',articleId)
    '''
@ajax_required
@login_required
@require_POST
def user_follow(request):
    #异步刷新(AJAX)
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        user = Userprofile.objects.get(id=user_id)
        try:
            if action == 'follow':
                Contact.objects.get_or_create(from_user=request.user.profile,to_user=user)
                create_action(request.user, '关注',user)
            else:
                Contact.objects.filter(from_user=request.user.profile,to_user=user).delete()
            return JsonResponse({'status':'ok'})
        except Userprofile.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
class RssFeed(Feed):
    title = "Rss订阅文章"
    link = "/"
    description = "这是zzr的博客文章"
    def items(self):
        return Article.objects.all()
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return item.content
    
    def item_link(self, item):
        return reverse('article')
    
    
@login_required
def User_Daily_Click(request):
    if Check_Daily_Click(request)==False:
        if request.user.is_active:
                create_click_oj = Daily_click(user=request.user.profile,click_status=True,created_time=timezone.now())
                create_click_oj.save()
                # 签到加饼果
                User = get_object_or_404(Userprofile, user=request.user)
                User.bonuspoints += 10 
                User.save()
    return redirect('main_article:article')

def archive(request):
    template = 'main_article/archive.html'
    articles_archive = Article.objects.all()
    context = {'articles_archive':articles_archive}
    return render(request,template,context)
        
    
# Create your views here.    