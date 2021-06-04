import re
# Utils.save2html('torrent.html',Utils.getRequest('https://exhentai.org/gallerytorrents.php?gid=1923317&t=fa1a4ce670'))
import time

from bs4 import BeautifulSoup

import Utils
import dl
import size_to_b
import torrent2magnet


class torrent_info:
    Size = 0
    Downloads = 0
    Seeds = 0
    Peers = 0
    torrent_address = ''


def download(ex_info, mode):
    MaxSize = 0  # 最大的Size
    MaxDownloads = 0  # 最大的Downloads
    MaxSeeds = 0  # 最大的Seeds
    MaxPeers = 0  # 最大的Peers
    torrent_info_list = []
    r = Utils.getRequest(ex_info.torrent_address)
    soup = BeautifulSoup(r.text, 'html.parser')
    # 遍历table
    for i in soup.find_all('table'):
        s = torrent_info()
        # 遍历td
        for k in i.find_all('td'):
            str_k = str(k)
            # 获取Size
            if re.search('Size:', str_k):
                size = Utils.getSODString(k)
                size = size_to_b.convert(size)
                if MaxSize < size:
                    MaxSize = size
                    s.Size = MaxSize
            # 获取Downloads
            elif re.search('Downloads', str_k):
                [s.extract() for s in k('span')]
                Downloads = int(k.text.strip())
                if MaxDownloads < Downloads:
                    MaxDownloads = Downloads
                    s.Downloads = MaxDownloads
            # 获取Seeds
            elif re.search('Seeds', str_k):
                [s.extract() for s in k('span')]
                Seeds = int(k.text.strip())
                if MaxSeeds < Seeds:
                    MaxSeeds = Seeds
                    s.Seeds = MaxSeeds
            # 获取Peers
            elif re.search('Peers', str_k):
                [s.extract() for s in k('span')]
                Peers = int(k.text.strip())
                if MaxPeers < Peers:
                    MaxPeers = Peers
                    s.Peers = MaxPeers
            # 获取 种子的链接
            elif re.search('<a href="https://exhentai.org/torrent/', str_k):
                table_tr_td_a_onclick = k.find('a')['onclick']
                table_tr_td_a_onclick = re.findall("document.location='(.+?)'", table_tr_td_a_onclick)[0]
                # table_tr_td_a_href = k.find('a')['href']
                s.torrent_address = table_tr_td_a_onclick
        # 将获取到的数据插入到List
        torrent_info_list.append(s)
    # 遍历List 获取 正确下载地址
    for i in torrent_info_list:
        if i.Size == MaxSize:
            time.sleep(1)
            # 下载种子
            r = Utils.getRequest(i.torrent_address)
            magnet = torrent2magnet.convert(r.content)
            ex_info.magnet = magnet
            # mode  0 代表 数据库 不存在该条 则插入一条新数据
            if mode == 0:
                dl.download(ex_info)
            # mode  1 代表 数据库 存在该条 但没有magnet 需要插入magnet
            elif mode == 1:
                print()
            time.sleep(1)
            # 写入文件 下载种子 (废弃)
            # path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'torrent' + os.sep
            # if not os.path.exists(path):
            #    os.mkdir(path)
            # with open(path + ex_info.file_name + '.torrent', 'wb') as file:
            #    file.write(r.content)
            #    file.close()
            break  # 防止有相同大小的Size 重复进行下载
