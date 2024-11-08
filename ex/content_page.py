import os
import re
import sys

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
    category = ""
    uploader = ""
    uploader_url = ""
    Posted = ""
    Language = ""
    Length = ""


def get_TAG_LIST(url):
    print("抓取地址为:".format(url))
    ex_gd3_ = ex_gd3()
    r = Utils.getRequest(url)
    # 如果页面已经被删除，则跳过该页面，写入为已抓取
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        # 开始获取gd3内容
        div_gd3 = soup.find('div', id='gd3')
        div_gdn_a  = div_gd3.find('div', id='gdn').find('a')
        ex_gd3_.uploader = div_gdn_a.text # 获得gd3下的uploader
        ex_gd3_.uploader_url = div_gdn_a.get('href') # 获得gd3下的uploader_url
        ex_gd3_.category= div_gd3.find('div',id="gdc").text# 获得 gdc下的category
        # 遍历 gd3 的tr条目
        for i in div_gd3.find_all('tr'):
            tag = str(i)
            # 获得gd3下的Posted
            if re.search('Posted:',tag):
                ex_gd3_.Posted = i.find('td',class_='gdt2').text
            # 获得gd3下的Language
            elif re.search('Language:',tag):
                ex_gd3_.Language = i.find('td',class_='gdt2').text
            # 获得gd3下的Length
            elif re.search('Length:',tag):
                ex_gd3_.Length = i.find('td',class_='gdt2').text
        # 开始获取 TAG内容
        div_taglist = soup.find('div', id='taglist')
        div_taglist_tr = div_taglist.find_all('tr')
        new_tag_list = ex_tag_list()  # 创建ex_tag_list
        # 遍历TAG tr
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
        SQLUTILS.updateSQL_TAG(url, new_tag_list,ex_gd3_)
        SQLUTILS.insertSQL_gd3(url,ex_gd3_)
    except:
        # 报错或没有任何TAG，则直接不抓取
        Mysqldb.updateSQL_delete(url)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        exception_info = "Exception Type: {}\nException Object: {}\nLine Number: {}\nURL:{}".format(exc_type,exc_obj,exc_tb.tb_lineno,url)
        # 将异常信息写入到文件中
        with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"error.log", "a") as file:
            file.write(exception_info)