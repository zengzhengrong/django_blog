from populate import base
from main_article.models import Article,Category,Contact,Userprofile
from django.contrib.auth.models import User

def create_contact():
    user1 = Userprofile.objects.get(id=1)
    user2 = Userprofile.objects.get(id=4)
    print(user1,user2)
    c1 = Contact.objects.create(from_user=user2,to_user=user1)
    c1.save()

    print('done')
if __name__ == '__main__':
    create_contact()   