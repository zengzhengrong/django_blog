import re
from django.template.defaultfilters import striptags
from django.utils.html import strip_tags
from django.conf import settings
# 生成文章目录
    
def get_catalog_math(content):
    '''
    Get html tags 
    '''
    pattern = re.compile('<h\d.*</h\d>')
    math = pattern.findall(content)# list[math1,math2]
    return math

def get_markdown_lines(content):
    line_list = content.splitlines()
    strip_lines = [title.strip() for title in line_list]
    return strip_lines

def get_filter_markdown_lines(content):
    '''
    Get markdown syntax 
    '''
    tag_title,tag_subtitle = getattr(settings,'SET_CATALOG_ID',('h4','h5'))
    md_title_num = '#'*int(tag_title.strip('h'))
    md_subtitle_num = '#'*int(tag_subtitle.strip('h'))
    md_lines = get_markdown_lines(content) # md
    filter_titles = [title for title in md_lines if title.startswith(md_title_num) or title.startswith(md_subtitle_num)]
    return filter_titles


def make_catalog_mark(content):
    content_list = list(content)
    start = 0
    for add_id in range(content_list.count('h')):
        try:
            index_h = content_list.index('h',start)
            if content_list[index_h-1] =='<' and content_list[index_h-1] !='/':
                content_list.insert(index_h+2, ' id')
            start = index_h+1
        except:
            break
    return content_list
def replace_catalog_mark(content):
    # is markdown add '<textarea>' tag 
    math =get_catalog_math(content)
    md_math = get_filter_markdown_lines(content)
    is_md = True if len(md_math) !=0 else False
    if is_md:
        content = '<textarea>{}</textarea>'.format(content)
    if len(math) == 0 and len(md_math) ==0:
        return None
    # make mark
    content_list = make_catalog_mark(content)
    try:
        start_name = 0
        if content_list.count(' id') == len(math):
            for subtitle_index in range(len(math)):
                math_replace = strip_tags(math[subtitle_index].replace('：' \
                if math[subtitle_index].find(':') == -1 else ':',''))
                id_index = content_list.index(' id', start_name)
                start_name = id_index+1
                idname = content_list[id_index].replace('id','id={}'.format(math_replace))
                del content_list[id_index]
                content_list.insert(id_index,idname)
                # print(idname)
                # print(content_list)
    except Exception as e:
        print(e)
    return content_list

def get_article_content(content):
    get_content_list = replace_catalog_mark(content)
    if get_content_list is None :
        return content
    content = ''.join(get_content_list)
    return content

def get_math(content):
    tag_title,tag_subtitle = getattr(settings,'SET_CATALOG_ID',('h4','h5'))
    md_title_num = '#'*int(tag_title.strip('h'))
    md_subtitle_num = '#'*int(tag_subtitle.strip('h'))
    math = get_catalog_math(content) # html
    filter_titles = get_filter_markdown_lines(content)

    if len(math) ==0 and len(filter_titles) ==0:
        return None
    if len(math) == 0 and len(filter_titles) !=0: # 没有匹配到则开始检测MarkDown
        tag_titles = []
        tag = None
        title_len = len(filter_titles)
        for title_index in range(title_len):
            # print('-'*title_len)
            md_title = filter_titles[title_index]

            if md_title.count(md_subtitle_num) == 1: # 先检测子标题后检测父标题
                tag = tag_subtitle
            if md_title.count(md_title_num) == 1 and tag is None:
                tag = tag_title

            replaced = md_title_num + ' '
            new = '<{tag}>{title}</{tag}>'.format(title=md_title.strip(replaced),tag=tag)
            tag_titles.append(new)
            tag = None
            # print(tag_titles)
            # time.sleep(.5)
        del filter_titles[-title_len:] # 清空列表释放内存
        return tag_titles
    return math