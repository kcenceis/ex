import time

import SQLUTILS
import Utils

maxPage = 5  # 每次运行抓取的页面数

if __name__ == '__main__':
    # r = Utils.getRequest('https://exhentai.org/')
    # Utils.getgl1c(r.text)
    SQLUTILS.connSQL()
    SQLUTILS.DeleteSQL()
    exhentai_url = 'https://exhentai.org/'
    params = 'f_cats=705'
    f_cats = '705'
    for i in range(0, maxPage):
        if i == 0:
            r = Utils.getPage(exhentai_url, params={
                'f_cats': f_cats
            })
        else:
            r = Utils.getPage(exhentai_url, params={
                'page': str(i),
                'f_cats': f_cats
            })
            print(r.url)
        Utils.getgl1c(r.text)
        time.sleep(1.5)
