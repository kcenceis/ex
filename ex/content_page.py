import re

from bs4 import BeautifulSoup

import Mysqldb
import SQLUTILS
import Utils


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
    reclass = ""


class ex_gd3:
    uploader = ""
    uploader_url = ""
    Posted = ""
    Language = ""
    Length = ""


def get_TAG_LIST(url):
    ex_gd3_ = ex_gd3()
    r = Utils.getRequest(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    div_gd3 = soup.find('div', id='gd3')
    div_gdn_a  = div_gd3.find('div', id='gdn').find('a')
    ex_gd3_.uploader = div_gdn_a.text
    ex_gd3_.uploader_url = div_gdn_a.get('href')
    for i in div_gd3.find_all('tr'):
        tag = str(i)
        if re.search('Posted:',tag):
            ex_gd3_.Posted = i.find('td',class_='gdt2').text
        elif re.search('Language:',tag):
            ex_gd3_.Language = i.find('td',class_='gdt2').text
        elif re.search('Length:',tag):
            ex_gd3_.Length = i.find('td',class_='gdt2').text
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
            new_tag_list.cosplayer = tag_list[:-1]
        elif re.search('^mixed:$', tag):
            new_tag_list.mixed = tag_list[:-1]
        elif re.search('^other:$', tag):
            new_tag_list.other = tag_list[:-1]
        elif re.search('^reclass:$', tag):
            new_tag_list.reclass = tag_list[:-1]
    SQLUTILS.updateSQL_TAG(url, new_tag_list)
    SQLUTILS.insertSQL_gd3(url,ex_gd3_)
