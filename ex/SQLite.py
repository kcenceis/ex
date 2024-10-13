import os
import sqlite3

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
       category       CHAR(200),
       language       CHAR(2000),
       parody         CHAR(2000),
       character      CHAR(2000),
       _group          CHAR(2000),
       artist         CHAR(2000),
       male           CHAR(2000),
       female         CHAR(2000),
       misc           CHAR(2000),
       _delete         INT(4),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        conn.commit()
        conn.close()
    if not check_table('filter_list'):
        conn = sqlite3.connect(SQLDATABASEFILE)
        c = conn.cursor()
        # 执行创建表
        c.execute('''CREATE TABLE filter_list                      
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
       tag_list         CHAR(2000),
       tag           CHAR(2000),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        conn.commit()
        conn.close()


def insertSQL(ex_info):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("INSERT INTO ex (title,address,torrent_address,magnet,file_name,category) VALUES (?,?,?,?,?,?)",
              (ex_info.title,
               ex_info.address,
               ex_info.torrent_address,
               ex_info.magnet,
               ex_info.file_name,
               ex_info.category,))
    conn.commit()
    c.close()
    conn.close()


def updateSQL_magent(ex_info):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute("UPDATE ex SET  magnet = ?\
      where address = ? ",
              (ex_info.magnet,
               ex_info.address,))
    conn.commit()
    c.close()
    conn.close()


def updateSQL_TAG(address, ex_tag_list):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    c.execute(
        "UPDATE  ex SET  language=?,parody=?,_character=?,_group=?,artist=?,male=?,female=?,misc=?,cosplayer=?,mixed=?,other=?,data1=1 where address = ? ",
        (
            ex_tag_list.language,
            ex_tag_list.parody,
            ex_tag_list.character,
            ex_tag_list.group,
            ex_tag_list.artist,
            ex_tag_list.male,
            ex_tag_list.female,
            ex_tag_list.misc,
            ex_tag_list.cosplayer,
            ex_tag_list.mixed,
            ex_tag_list.other,
            address,))
    conn.commit()
    c.close()
    conn.close()


def selectSQL():
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    conn.commit()
    # 查询数据
    cursor = c.execute("SELECT *  from ex")
    # for row in cursor:
    #    print("ID = ", row[0])
    #    print("ADDRESS = ", row[1])
    return cursor.fetchall()
    # cursor.close()
    # conn.close()


def selectSQL_getex(ex_info):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    # 查询数据
    cursor = c.execute("SELECT count(*)  from ex where address=?", (ex_info.address,))
    # for row in cursor:
    #    print("ID = ", row[0])
    #    print("ADDRESS = ", row[1])
    return cursor.fetchone()
    # cursor.close()
    # conn.close()


def selectSQL_HAVETAG(ex_info):
    conn = sqlite3.connect(SQLDATABASEFILE)
    c = conn.cursor()
    cursor = c.execute('''SELECT count(*)  from ex where address=%s and _delete is NULL and data1 is NULL''',
                       (ex_info.address,))
    return cursor.fetchone()


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
        cursor = c.execute("delete from ex where date('now', '-7 day') >= date(dDate) and _delete='1'")  # 删除7日前的数据
        conn.commit()
        cursor.close()
        conn.close()
