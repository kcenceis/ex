# 模式为 MYSQL 和 SQLite
import Mysqldb
import SQLite

mode = "MySQL"


# 初始化SQLite数据库文件
def connSQL():
    if mode == "MySQL":
        Mysqldb.conn()
        Mysqldb.DeleteSQL()
    elif mode == "SQLite":
        SQLite.connSQL()
        SQLite.DeleteSQL()


def insertSQL(ex_info):
    if mode == "MySQL":
        Mysqldb.insertSQL(ex_info)
    elif mode == "SQLite":
        SQLite.insertSQL(ex_info)


def updateSQL_magent(ex_info):
    if mode == "MySQL":
        Mysqldb.updateSQL_magent(ex_info)
    elif mode == "SQLite":
        SQLite.updateSQL_magent(ex_info)


def updateSQL_TAG(address, ex_tag_list):
    if mode == "MySQL":
        Mysqldb.updateSQL_TAG(address, ex_tag_list)
    elif mode == "SQLite":
        SQLite.updateSQL_TAG(address, ex_tag_list)


def selectSQL_getex(ex_info):
    if mode == "MySQL":
        return Mysqldb.selectSQL_getex(ex_info)
    elif mode == "SQLite":
        return SQLite.selectSQL_getex(ex_info)

def insertSQL_gd3(address,ex_gd3):
    if mode == "MySQL":
        Mysqldb.insertSQL_gd3(address,ex_gd3)


def selectSQL_HAVETAG(ex_info):
    if mode == "MySQL":
        return Mysqldb.selectSQL_HAVETAG(ex_info)
    elif mode == "SQLite":
        return SQLite.selectSQL_HAVETAG(ex_info)


# 删除7日前的数据
def DeleteSQL():
    if mode == "MySQL":
        return Mysqldb.DeleteSQL()
    elif mode == "SQLite":
        return SQLite.DeleteSQL()
