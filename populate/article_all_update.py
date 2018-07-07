from populate import base
from main_article.models import Article,Category
from taggit.models import Tag
import random

def tagdelete():
    Tag.objects.all().delete()
    print('Delete..all')
if __name__ == '__main__':
    tagdelete()
def populate():
    print('update......')
    tag_names = ['web','django','game','python']   
    articles = Article.objects.all()
    for tag_name in tag_names:
        Tag.objects.get_or_create(name=tag_name)
    tag_populate_target1 = Tag.objects.get(name='web')
    tag_populate_target2 = Tag.objects.get(name='django')
    for article in articles:
        article.tags.add(tag_populate_target1)
        article.tags.add(tag_populate_target2)
        article.save()
    print('done')
if __name__ == '__main__':
    populate()  
'''
def tagCreate():
    print('tag is Creating...')
    for n in range(1000):
        Tag.objects.create(name=n)
        print('done')
    print('finish')
    print(Tag.objects.all().__len__())
if __name__ == '__main__':
    tagCreate()    
'''        
    