import json
import os
import re

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

import SQLUTILS
import content_page
import dl

proxies = "socks5://127.0.0.1:1080"
proxyON = False
SQLMode = "MySQL"  # 模式为SQLite MySQL
with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"config.json", "r") as f:
    result = json.loads(f.read())
    headers = {"User-Agent": result['User-Agent']}
    cookie = {'ipb_member_id': result['ipb_member_id'],
              'ipb_pass_hash': result['ipb_pass_hash'],
              'igneous': result['igneous'],
              'sk': result['sk']}


mReq = requests.session()
mReq.mount('https://', HTTPAdapter(max_retries=5))
mReq.mount('http://', HTTPAdapter(max_retries=5))


def initSQL():
    SQLUTILS.connSQL()
    SQLUTILS.DeleteSQL()


# 定义Request方法,request headers 和 proxy
def getRequest(http_url):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, cookies=cookie, timeout=10)
    else:
        r = mReq.get(url=http_url, headers=headers, cookies=cookie, timeout=10)
    # r.raise_for_status()
    return r


# 定义Request方法,request headers 和 proxy
def getPage(http_url, params):
    # 是否开启代理
    if proxyON:
        r = mReq.get(url=http_url, headers=headers, proxies=proxies, cookies=cookie, timeout=10, params=params)
    else:
        r = mReq.get(url=http_url, headers=headers, cookies=cookie, timeout=10, params=params)
    # r.raise_for_status()
    return r


# 将不能作为文件名的字符替换为下划线
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


# 将网页下载到文件 防止多次访问页面导致被封IP
def save2html(file_name, r):
    with open(file_name, 'w') as file:
        file.write(r.text)
        file.close()


# 字符处理
def getSODString(self):
    [s.extract() for s in self('span')]
    myNowTorrnet = self.text.replace(' ', '')  # 种子大小
    return myNowTorrnet


class ex_info:
    title = ''
    address = ''
    preview_address = ''
    torrent_address = ''
    file_name = ''
    magnet = ''
    category = ''


# 获取导航栏信息 返回指定数据(下一页的网址)
def getsearchnav(r):
    soup = BeautifulSoup(r, 'html.parser')
    searchnav = soup.find_all('div', class_='searchnav')
    ufirst = searchnav[0].find('a', id='ufirst')
    uprev = searchnav[0].find('a', id='uprev')
    ujumpbox = searchnav[0].find('a', id='ujumpbox')
    unext = searchnav[0].find('a', id='unext')
    ulast = searchnav[0].find('a', id='ulast')
    # print(ufirst)
    # print(uprev)
    # print(ujumpbox)
    # print(unext)
    # print(ulast)
    return unext['href']


# 获取预览页的信息
def getgl1c(r):
    #    isFinish = False
    bookList = []
    soup = BeautifulSoup(r, 'html.parser')
    str_cookies = cookie
    # 判断是否存在cookies：sk
    if cookie.get('sk') is not None:

        for div in soup.find_all('div', class_='gl3t'):
            s = ex_info()
            div_gl3t_a_href = div.find('a')['href']  # book 链接
            div_gl3t_img = div.find('img')  # div_gl3t_img

            preview_address = div_gl3t_img['src']
            title = div_gl3t_img['title']
            s.title = title
            s.address = div_gl3t_a_href
            s.preview_address = preview_address
            s.file_name = validateTitle(title)
            bookList.append(s)

        div_gldown = soup.find_all('div', class_='gldown')  # 种子页面链接
        div_gl5t = soup.find_all('div', class_='gl5t')  # category
        for i in range(0, len(div_gldown)):
            bookList[i].category = div_gl5t[i].find('div', class_='cs').text
            str_div = str(div_gldown[i])
            # 检查不到任何种子
            if re.search('title="No torrents available"', str_div):
                pass
            else:
                div_gldown_a_href = div_gldown[i].find('a')['href']  # torrent页面链接
                bookList[i].torrent_address = div_gldown_a_href
    else:
        for div in soup.find_all('td', class_='gl3c glname'):
            s = ex_info()
            # print(div)
            div_gl3c_a_href = div.find('a')['href']  # book 链接
            div_gl3t_img = div.find('img')  # div_gl3t_img
            # preview_address = div_gl3t_img['src']
            # title = div_gl3t_img['title']
            # s.title = title
            title = div.find('div', class_='glink').text  # 标题
            s.title = title
            s.address = div_gl3c_a_href
            # s.preview_address = preview_address
            s.file_name = validateTitle(title)
            bookList.append(s)
        # 抓取 预览图
        td_gl2c = soup.find_all('td', class_='gl2c')
        for i in range(0, len(td_gl2c)):
            td_gl2c_img = td_gl2c[i].find('img')
            if re.search('<img alt="(.+?)" data-src="(.+?)"', str(td_gl2c_img)):
                preview_address = td_gl2c_img['data-src']
            else:
                preview_address = td_gl2c_img['src']
            td_gl2c_gldown_a = td_gl2c[i].find('div', 'gldown').find('a')
            # 没有种子的网址
            if td_gl2c_gldown_a is None:
                pass
            # 获取到种子
            else:
                bookList[i].torrent_address = td_gl2c_gldown_a['href']
            # title = td_gl2c_img['alt'] 预览图中的标题 预留
            bookList[i].preview_address = preview_address

    for i in bookList:
        cursor = SQLUTILS.selectSQL_getex(i)  # 获取ex数据库内容
        # 防止已经下载过
        if cursor[0] == 0:
            dl.download(i)
        #else:
        #    count = SQLUTILS.selectSQL_HAVETAG(i)  # 确定是否已经获取到预览图，是否已经抓取过tag，是否已经抓取过，是否被删除过
        #    if count[0] != 0:
        #       content_page.get_TAG_LIST(i.address)
