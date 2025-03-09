import json
import os

import requests

# 读取confid.json
with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"config.json", "r") as f:
    result = json.loads(f.read())
    headers = {"User-Agent": result['User-Agent']}
    cookie = {'ipb_member_id': result['ipb_member_id'],
              'ipb_pass_hash': result['ipb_pass_hash']}
# 进行网页请求，获取新的cookies
mReq = requests.session()
r = mReq.get(url="https://exhentai.org/", headers=headers, cookies=cookie, timeout=10)
try:
    # 判断是否存在igneous
    if 'igneous' in r.cookies:
       result['igneous']=r.cookies.get('igneous')
       # 获取cookies成功，后写入到config.json
       with open('config.json', 'w') as outputfile:
           json.dump(result, outputfile, indent=4)
except:
    exit()
