import sqlite3
import os

SQLDATABASEFILE = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'ex.db'  # 数据库文件名称


# 传入数据表名称检查是否存在 返回True False
# param: 数据表名称
def check_table(table_name):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("select count(*) from sqlite_master where name=? ", (table_name,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 初始化SQLite数据库文件
def connSQL():
    if not check_table('ex'):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        # 执行创建表
        c.execute('''CREATE TABLE ex                      
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       title          CHAR(200),
       address        CHAR(2000),
       torrent_address        CHAR(2000),
       magnet         CHAR(2000),
       file_name      CHAR(2000),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        conn.commit()
        conn.close()


def insertSQL(ex_info):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO ex (title,address,torrent_address,magnet,file_name) \
      VALUES (?,?,?,?,?)",
              (ex_info.title,
               ex_info.address,
               ex_info.torrent_address,
               ex_info.magnet,
               ex_info.file_name,))
    conn.commit()
    c.close()
    conn.close()



def selectSQL():
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    conn.commit()
    # 查询数据
    cursor = c.execute("SELECT *  from ex")
    for row in cursor:
        print("ID = ", row[0])
        print("ADDRESS = ", row[1])
    cursor.close()
    conn.close()


# 获取有多少相同的地址，返回bool
def isFinish(mAddress):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*) as count  from ex where address = ?", (mAddress,))
    # values = cursor.fetchone()
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if result == 1:
        return True
    else:
        return False


# 删除7日前的数据
def DeleteSQL():
    if os.path.exists(SQLDATABASEFILE):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        cursor = c.execute("delete from ex where date('now', '-7 day') >= date(dDate)")  # 删除7日前的数据
        conn.commit()
        cursor.close()
        conn.close()
