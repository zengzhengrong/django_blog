import logging
import os
import re
from urllib import request

import jieba
from django.conf import settings
from django.template.defaultfilters import striptags
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from PIL import Image
from wordcloud import WordCloud

# 配置日志信息

class Thumbnail(ImageSpec):
    processors = [ResizeToFill(85, 85)]
    format = 'PNG'
    options = {'quality': 60}
class ThumbnailTitle(ImageSpec):
    processors = [ResizeToFill(615, 300)]
    format = 'PNG'
    options = {'quality': 60}
def save_title_img(fp,file_name,file_path=settings.MEDIA_ROOT +'/'+'title'):
    # 宽高比大于1，直接使用内容图片，小于1对照片进行裁剪，并另保存
    # 裁剪：
    # 修改大小和格式，并将修改后的图片放到title目录
    # file_name就是新图片名字以post.id命名
    
    try:
        #相对路径media/
        relative_fp = fp[1:] 
        #print(fp)

        # 宽高比大于1
        content_img_PIL = Image.open(relative_fp,'r')
        img_width_height = content_img_PIL.size
        #print('图片的高：{}'.format(img_width_height))
        content_img_PIL.close()
        if img_width_height[0]/img_width_height[1] > 1:
            return fp
        # 裁剪
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_suffix = '.png' 
        new_file_path = '{}{}{}{}'.format(file_path,'/',file_name,file_suffix)
        content_img = open(relative_fp,'rb')
        source = ThumbnailTitle(source=content_img)
        result = source.generate()
        new_img = open(new_file_path,'wb+')
        new_img.write(result.read())
        new_img.close()
        content_img.close()
    except IOError as e:
        print ('File operation failure',e)
        return None
    except Exception as e:
        print ('Erroroperation ：',e)
        return None
    return '/media/title/'+file_name+'.png'
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
            #down load finish
            request.urlretrieve(img_url, filename=filename)
            #alter img
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

def frist_img(content,filename):
    img_pattern = re.compile('<img.*?>')
    path_pattern = re.compile('/media/.*?"')
    http_pattern = re.compile('http.*?"')
    img_math = img_pattern.findall(content)
    #print(img_math)
    # 匹配不到img标签，返回None
    if len(img_math) == 0:
        return None
    # 检测匹配第一个img标签是否为网络图片，是的话返回图片url
    frist_img = img_math[0]
    if 'http' in frist_img:
        http_math = http_pattern.findall(frist_img)
        http_img = http_math[0].strip('"')
        #print(http_img)
        return http_img
    # 检测本地路径图片
    path_math = path_pattern.findall(frist_img)
    path_img = path_math[0].strip('"')
    # 调用另存为图片函数
    new_img = save_title_img(path_img,str(filename))
    return new_img

def img_wordcloud(title,filename,file_path=settings.MEDIA_ROOT +'/'+'title'):
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        path_ttf = "main_article/static/main_article/ttf/MSYH.TTF"
        file_path = '/media/title/' + str(filename) + '.png'
        seg_list = jieba.cut(title)  # 默认是精确模式
        # print(seg_list)
        word_text = " ".join(seg_list)
        # print(word_text)
        wordcloud = WordCloud(font_path=path_ttf,width=615,height=300,background_color='white').generate(word_text)
        wordcloud.to_file('media/title/' + str(filename) + '.png')     
    except Exception as e:
        print(e)
        return None
    return file_path

def custom_img(img):
    print(img)
    return '/media/title/'+ str(img)
