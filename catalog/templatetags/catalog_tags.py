import re
import time
from django import template
from django.template.defaultfilters import striptags
from django.utils.safestring import mark_safe
from django.conf import settings
from ..catalog import *

register = template.Library()
@register.simple_tag
def render_catalog_html(content):
    math = get_math(content)
    if math is None:
        return None
    html_attr = getattr(settings,'SET_CATALOG_ATTR',{})
    ul_attr = html_attr.get('ul','')
    li_attr = html_attr.get('li','')
    title,subtitle = getattr(settings,'SET_CATALOG_ID',('h4','h5'))

    html = '<ul {}>'.format(ul_attr)
    for subtitle_index in range(len(math)):
        math_replace = math[subtitle_index].replace('：' if math[subtitle_index].find(':') == -1 else ':','')

        if math[subtitle_index].startswith('<'+title):
            html += '<li {}><a href="#{}">{}</a></li>'.format(
                                                        li_attr,
                                                        striptags(math_replace),
                                                        striptags(math_replace))
        
        if math[subtitle_index].startswith('<'+subtitle):
            html += '<ul {}><li {}><a href="#{}">{}</a></li></ul>'.format(
                                                                ul_attr,
                                                                li_attr,
                                                                striptags(math_replace),
                                                                striptags(math_replace))
    html +='</ul>'
    return html
@register.filter(name='catalog')
def get_post_content(content):
    content = get_article_content(content)
    return mark_safe(content)