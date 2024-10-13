import Mysqldb
import SQLUTILS
import content_page

# 初始化数据库
SQLUTILS.connSQL()

# 获取没有tag的条目
# 返回address
result = Mysqldb.selectSQL_untag()

# 传入address循环抓取tag
for i in result:
       content_page.get_TAG_LIST(i[0])
