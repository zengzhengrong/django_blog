from populate import base
from django.contrib.auth.models import User
from online_status.models import OnlineStatus
from django.core.cache import cache
def populate():
    print('delete online status or redis cache')
    users = User.objects.all()
    for user in users:
        username_cache = '{}_last_login'.format(user.username)
        if cache.has_key(username_cache):
            print('has key')
            OnlineStatus.objects.all().delete()
            cache.delete(username_cache)
            print('cache delete')
    print('Creating admin account...', end='')
    User.objects.all().delete()
    User.objects.create_superuser(username='admin', password='admin', email=None)
    print('done')
if __name__ == '__main__':
    populate()