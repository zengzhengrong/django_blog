from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
import functools
#python装饰器


def admin_required(func):
    def auth(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request, message='暂不开放')
            return redirect('main_article:article')
        return func(request,*args,**kwargs)
    return auth

def author_required(func):

    @functools.wraps(func)
    def auth(request,*args,**kwargs):
        print(dir(func))
        print(func.__dict__)
        print(func.__name__)
        print(func.__doc__)
        result = func(request,*args, **kwargs)
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))    
        print(arg_lst)
        print(result)
        if not request.user:
            messages.error(request,'你没有权限')
            return redirect('main_article:article')
        return func(request,*args,**kwargs)
    return auth
def ajax_required(func):
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return func(request, *args, **kwargs)
    wrap.__doc__=func.__doc__
    wrap.__name__=func.__name__
    return wrap