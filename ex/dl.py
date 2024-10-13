import os
import re
import time

import SQLUTILS
import Utils

filePath = os.path.split(os.path.realpath(__file__))[0]  # 获取脚本当前目录


def download(ex_info):
    # 下载预览图之前获取页面的所有TAG
    time.sleep(1)  # 防止被封IP
    # 执行下载
    path = filePath + os.sep + 'Preview' + os.sep
    if not os.path.exists(path):
        os.mkdir(path)
    img_format = re.findall('\.(jpg|bmp|png|jpeg|webp|gif)', ex_info.preview_address)[0]
    r = Utils.getRequest(ex_info.preview_address)
    ex_info.file_name = ex_info.file_name + '.' + img_format
    with open(path + ex_info.file_name, 'wb') as file:
        file.write(r.content)
        file.close()
        SQLUTILS.insertSQL(ex_info)
