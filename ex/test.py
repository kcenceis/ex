import json

import SQLUTILS
import content_page
from Utils import ex_info

#json.loads()

SQLUTILS.connSQL()
z = ex_info()
z.address = 'https://exhentai.org/g/3086451/41ecffa2e0/'
ex_tag_list = content_page.get_TAG_LIST(z.address)

# if zx is None:
#    print("asdasd")
# else:
#    if zx[0] is None:
#       print("asdasdasdasd")
