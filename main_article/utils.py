import os
import logging
from urllib import request
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from blog import settings
import re
from django.template.defaultfilters import striptags
# 配置日志信息

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(85, 85)]
    format = 'PNG'
    options = {'quality': 60}

def save_avatar_img(img_url,file_name,file_path=settings.MEDIA_ROOT +'/'+'github_avatar'):
    try:
        print('doing..download..img')
        full_path = file_path+'/'+file_name
        if not os.path.exists(full_path):
            print(file_path + ',path not found ,rebuild')
            os.makedirs(full_path)
            print('mkdir..githubavatarfolder.success')
            file_suffix = '.png'      
            filename = '{}{}{}{}'.format(full_path,'/',file_name,file_suffix)
            request.urlretrieve(img_url, filename=filename)     
            read_github_avatar = open(filename,'rb')
            result=Thumbnail(source=read_github_avatar).generate()
            avatar_85 = open(filename, 'wb')     
            # file_path+os.sep+file_name+'avatar_85.png'
            avatar_85.write(result.read())
            avatar_85.close()
            print('download img success ')
            print(avatar_85)    
    except IOError as e:
        print ('File operation failure',e)
    except Exception as e:
        print ('Erroroperation ：',e)
    return '/github_avatar/'+file_name+'/'+ file_name +'.png'
def title_list(content):
    pattern = re.compile(r'<h\d.*</h\d>')
    
    math = pattern.findall(content)
    html = '<ul>'
    # print(math)
    # print('')
    for subtitle_index in range(len(math)):
        math_replace = math[subtitle_index].replace('：' if math[subtitle_index].find(':') == -1 else ':','')
        # print(True if math[subtitle_index].find(':') else False)
        if math[subtitle_index].startswith('<h4'):
            html += '<li><a href="#{}">{}</a></li>'.format(striptags(math_replace),striptags(math_replace))
        if math[subtitle_index].startswith('<h5'):
            html += '<ul><li><a href="#{}">{}</a></li></ul>'.format(striptags(math_replace),striptags(math_replace))
    html +='</ul>'
    return html
