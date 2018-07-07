from easy_comment.forms import CommentForm
from easy_comment.models import Comment, Like
from django.http import JsonResponse
from django.views.decorators.http import require_POST
#from django.shortcuts import render,redirect
from . import handlers
from activity_stream.utils import create_action
# Create your views here.

@require_POST
def submit_comment(request, id):
    form = CommentForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        # print('success')
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.user_name =  request.user.profile.nickname if request.user.profile.nickname else request.user
        #print(new_comment.user_name)
        new_comment.save()
        #action create
        create_action(request.user, '发表了评论', new_comment)
        location = "#c" + str(new_comment.id)
        return JsonResponse({'msg':'success!', 'new_comment':location})
    return JsonResponse({'msg':'评论出错!'})
    

@require_POST
def like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')
    if comment_id and action:
        try:
            comment = Comment.objects.get(id=comment_id)
            obj, created = Like.objects.get_or_create(user = request.user, comment = comment)
            if action == 'like':
                if not created:
                    obj.status = True
                    obj.save()
                    #print(obj)
                    create_action(request.user, '点赞了评论', obj)
            if action == 'cancel-like' or action == 'cancel-dislike':
                obj.delete()
            if action == 'dislike':
                obj.status = False
                obj.save()
            return JsonResponse({'msg':'OK'})
        except Comment.DoesNotExist:
            return JsonResponse({"msg":"KO"})
    return JsonResponse({"msg":"KO"})