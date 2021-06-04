import time

import SQLUTILS
import Utils

maxPage = 20  # 最大页面数

if __name__ == '__main__':
    # r = Utils.getRequest('https://exhentai.org/')
    # Utils.getgl1c(r.text)
    SQLUTILS.connSQL()
    exhentai_url = 'https://exhentai.org/'
    f_cats = '705'
    for i in range(0, maxPage):
        if i == 0:
            r = Utils.getPage(exhentai_url, params={
                'f_cats': f_cats
            })
        else:
            r = Utils.getPage(exhentai_url, params={
                'page:': str(i),
                'f_cats': f_cats
            })
        # file = open('ex.html', 'r')
        # html = file.read()
        Utils.getgl1c(r.text)
        time.sleep(1.5)
