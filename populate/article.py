from populate import base
from main_article.models import Article,Category
from easy_comment.models import Comment
from django.contrib.auth.models import User

import random


def populate():
    
    print('article..delete')
    Article.objects.all().delete()
    print('populating....',end='')
    titles = [
    'C++',
    'C#',
    'C',
    'Python',
    'Java',
    'go',
    'ruby',
    'shell',
    'JavaScript',
    'html5',
    'css5',
    'php',
    'R',
    'MATLAB',
    'Perl',
    'Objective-C',
    'VB',
    'sql',
    'Swift',
    'Lisp',
    'Pascal',
    'Ruby',
    'SAS',
    'Erlang',
    'OpenCL'
    ]

    comment = 'nice language'
    category,created = Category.objects.get_or_create(name='计算机语言')
    print('delete..article..reload')
    articles  = Article.objects.filter(category=category)
    articles.delete()
    print('delete...done')
    user = User.objects.get(username='admin')
    for title in titles:
        article = Article()
        article.title = title
        for n in range(10):
            article.content += title + '\n'
        article.likes = random.randint(0,99)
        article.read_num = random.randint(0,99)
        article.author = user
        article.category = Category.objects.get(name = '计算机语言')
        article.save()
        print('begin..createComment')
        Comment_everyone,created = Comment.objects.get_or_create(user=user,content=comment,post=article)
       
    print('done')

if __name__ == '__main__':
    populate()
