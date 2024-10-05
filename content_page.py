import re

import Utils
from bs4 import BeautifulSoup


class ex_tag_list:
    language = ""
    parody = ""
    character = ""
    group = ""
    artist = ""
    male = ""
    female = ""
    misc = ""
    cosplayer = ""
    mixed = ""
    other = ""


def get_TAG_LIST(url):
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_taglist = soup.find('div', id='taglist')
    div_taglist_tr = div_taglist.find_all('tr')
    new_tag_list = ex_tag_list()  # 创建ex_tag_list
    # 遍历TAG
    for i in div_taglist_tr:
        tag_list = ""
        # 获取tag中TAG内容
        for k in i.find_all('div'):
            tag_list = tag_list + k.text + ','

        # 获取TAG头
        tag = i.find('td', class_='tc').text
        tag = str(tag)
        if re.search('^language:$', tag):
            new_tag_list.language = tag_list[:-1]
        elif re.search('^parody:$', tag):
            new_tag_list.parody = tag_list[:-1]
        elif re.search('^character:$', tag):
            new_tag_list.character = tag_list[:-1]
        elif re.search('^group:$', tag):
            new_tag_list.group = tag_list[:-1]
        elif re.search('^artist:$', tag):
            new_tag_list.artist = tag_list[:-1]
        elif re.search('^male:$', tag):
            new_tag_list.male = tag_list[:-1]
        elif re.search('^female:$', tag):
            new_tag_list.female = tag_list[:-1]
        elif re.search('^misc:$', tag):
            new_tag_list.misc = tag_list[:-1]
        elif re.search('^cosplayer:$', tag):
            new_tag_list.misc = tag_list[:-1]
        elif re.search('^mixed:$', tag):
            new_tag_list.misc = tag_list[:-1]
        elif re.search('^other:$', tag):
            new_tag_list.misc = tag_list[:-1]
    # 返回内容
    return new_tag_list
