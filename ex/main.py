import time

import Utils

maxPage = 10  # 每次运行抓取的页面数

if __name__ == '__main__':
    # r = Utils.getRequest('https://exhentai.org/')
    # Utils.getgl1c(r.text)
    # SQLUTILS.connSQL()
    # SQLUTILS.DeleteSQL()
    Utils.initSQL()
    exhentai_url = 'https://exhentai.org/'
    params = 'f_cats=641'
    unext = ""
    for i in range(0, maxPage):
        if i == 0:
            r = Utils.getPage(exhentai_url, params)
        else:
            r = Utils.getRequest(unext)
            # r = Utils.getPage(exhentai_url, params={
            #    'page': str(unext)
            # })
        print(r.url)
        if i != maxPage:
            unext = Utils.getsearchnav(r.text)
        Utils.getgl1c(r.text)
        time.sleep(1.5)
