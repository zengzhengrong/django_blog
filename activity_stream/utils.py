import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user,verb,action=None):
    '''
        避 免重复操作：保存前1分钟，只取回最早一个相同操作
    last_minute :的显示为当前django。setting的USE_TZ=True的前60秒的时间轴
    same_actions :先筛选出符合前两个变量和在此时间轴的动作(即没有关联模型)
        然后在判断是否有关联动作
        有的话则再次从same_actions中筛选出有此关联模型的动作(即此时same_actions含有关联模型)
    然后判断是否有same_actions(即判断是否已存在的相同动作)
            有:则此函数不生效 return False
            无:则创建一个新动作return True
    '''
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    #print(last_minute)
    same_actions = Action.objects.filter(user=user,verb=verb,created__gte=last_minute)#大于前一分钟保存过的动作
    if action:
        action_ct = ContentType.objects.get_for_model(action)
        same_actions = same_actions.filter(action_ct=action_ct,ct_id=action.id)
    if not same_actions:
        action_ensure = Action(user=user,verb=verb,action=action)
        action_ensure.save()
        return True
    return False
    