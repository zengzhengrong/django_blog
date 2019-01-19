from django.shortcuts import render, get_object_or_404,redirect
from guestbook.models import Guestbook_Post,Guestbook_Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from guestbook.forms import PostForm
from django.utils import timezone
from django.contrib import messages
from activity_stream.utils import create_action
from django.contrib.auth.decorators import login_required

@login_required
def guestbook_index(request):
    template = 'guestbook/index.html'
    guestbook_posts = Guestbook_Post.objects.all()   
    #分页显示
    paginator = Paginator(guestbook_posts,8)
    page = request.GET.get('page')
    try:
        guestbook_posts = paginator.page(page)
    except PageNotAnInteger:
        guestbook_posts = paginator.page(1)
    except EmptyPage:
        guestbook_posts = paginator.page(paginator.num_pages)
    context = {'guestbook_posts':guestbook_posts,
               'articlecount':guestbook_posts.__len__(),
               'guestbook_posts_session':'guestbook'
               }
    return render(request, template, context)

def guestbook_Post_Read(request,postId):
    if request.method == 'GET':
        template = 'guestbook/PostRead.html'
        post = get_object_or_404(Guestbook_Post,id=postId)
        post.read_num +=1
        post.save()
    context = {'post':post,
               'guestbook_posts':'cut-articleCreate-link',
               'guestbook_posts_session':'guestbook'
                }
    return render(request, template, context)
    
def guestbook_Post_Create(request):
    template = 'guestbook/PostCreateUpdate.html'
    if request.method == 'GET':       
        return render(request, template,{'postform':PostForm(),'guestbook_posts':'cut-articleCreate-link','guestbook_posts_session':'guestbook'})
    #Post
    postform = PostForm(request.POST)   
    if not postform.is_valid():
        return render(request, template, {'postform':postform})  
    author_id = request.user  
    form = postform.save(commit=False)    
    form.author = author_id
    form.upDateTime = timezone.now()
    form.save()
    #save tags
    postform.save_m2m()
    #action create
    create_action(request.user,'发表了留言', form)
    
    messages.success(request,'文章已新增')
    return redirect('guestbook:posts')
def guestbook_Post_Update(request,postId):
    get_post = get_object_or_404(Guestbook_Post,id=postId)
    if request.method =='GET':
        template = 'guestbook/PostCreateUpdate.html'
        update_post = PostForm(instance=get_post)       
        return render(request, template, {'postform':update_post,'post':get_post,'guestbook_posts_session':'guestbook'})
    #Post
    
    post_update = PostForm(request.POST,instance=get_post)
    if not post_update.is_valid():
        return render(request, template, {'postform':post_update,'post':get_post})
    post_update_Form = post_update.save(commit=False)   
    post_update_Form.upDateTime = timezone.now()
    post_update_Form.save()
    post_update.save_m2m()
    create_action(request.user,'修改了留言', post_update_Form)    
    messages.success(request, '文章已修改')
    return redirect('guestbook:postRead', postId)
def guestbook_Post_Delete(request,postId):
    post_delete = get_object_or_404(Guestbook_Post,id=postId)
    post_delete.delete()
    post_delete_str = str(post_delete)
    create_action(request.user,'删除了留言-'+post_delete_str,post_delete)
    messages.success(request, '留言已删除')
    return redirect('guestbook:posts')


def g_categoryRead(request,g_categoryId):
    template = 'guestbook/index.html'
    guestbook_posts = Guestbook_Post.objects.filter(category=g_categoryId)
    paginator = Paginator(guestbook_posts,8)
    page = request.GET.get('page')
    try:
        guestbook_posts = paginator.page(page)
    except PageNotAnInteger:
        guestbook_posts = paginator.page(1)
    except EmptyPage:
        guestbook_posts = paginator.page(paginator.num_pages)
        
    context = {'guestbook_posts':guestbook_posts,            
               'articlecount':guestbook_posts.__len__(),
               'guestbook_posts_session':'guestbook'
               }
    return render(request, template,context)
def g_categoryDelete(request,g_categoryId):
        #POST
    category = get_object_or_404(Guestbook_Category,id=g_categoryId)
    category_str = str(category)
    category.delete()
    create_action(request.user, '删除了留言分类'+'-'+category_str,category)
    messages.success(request, '板块已删除')
    
    return redirect('main_article:categoryControl')

@login_required
def g_categoryUpdate(request,g_categoryId):
    template = 'main_article/categoryUpdate.html'
    category = get_object_or_404(Guestbook_Category,id=g_categoryId)
    if request.method == 'GET':
        return render(request, template,{'category':category,'page_title':'更新留言分类'})
    #POST
    content = request.POST.get('content')
    category.name = content
    category.save()
    create_action(request.user, '修改了分类',category)
    #print(content)
    messages.success(request,'板块已修改')
    return redirect('main_article:categoryControl')
# Create your views here.
