import mysql.connector

host = "db"
user = ""
password = ""
db = "ex"


def initMySQL():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db
    )
    return mydb


# 传入数据表名称检查是否存在 返回True False
# param: 数据表名称
def check_database(database):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = mydb.cursor()
    database = (database,)
    sql = "SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = %s ;"
    cursor.execute(sql, database)
    if cursor.fetchone()[0] == 1:
        mydb.close()
        return True
    else:
        cursor.execute("CREATE DATABASE "+db)
        mydb.commit()
        mydb.close()
        return False


# 创建数据库
def conn():
    if not check_database(db):
        mydb = initMySQL()
        cursor = mydb.cursor()
        cursor.execute('''
        CREATE TABLE ex                      
        (id INT PRIMARY KEY AUTO_INCREMENT,
       title                VARCHAR(200),
       address              text,
       torrent_address      text,
       magnet               text,
       file_name            text,
       category             text,
       language             text,
       parody               text,
       _character           text,
       _group               text,
       artist               text,
       male                 text,
       female               text,
       misc                 text,
       _delete              INT(4),
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data1               text,
        data2               text,
        data3               text,
        data4               text
        );
        ''')
        # 执行创建表
        cursor.execute('''
        CREATE TABLE filter_list                      
       (id INT PRIMARY KEY AUTO_INCREMENT,
       tag_list         text,
       tag              text,
       dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       );''')
        mydb.commit()
        mydb.close()


def insertSQL(ex_info, ex_tag_list):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ex (title,address,torrent_address,magnet,file_name,category,language,parody,_character,"
              "_group,artist,male,female,misc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (
                ex_info.title,
                ex_info.address,
                ex_info.torrent_address,
                ex_info.magnet,
                ex_info.file_name,
                ex_info.category,
                ex_tag_list.language,
                ex_tag_list.parody,
                ex_tag_list.character,
                ex_tag_list.group,
                ex_tag_list.artist,
                ex_tag_list.male,
                ex_tag_list.female,
                ex_tag_list.misc,))
    conn.commit()
    conn.close()

def updateSQL_magent(ex_info):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''UPDATE ex SET  magnet = %s where address = %s ''', (ex_info.magnet,
               ex_info.address,))
    conn.commit()
    cursor.close()
    conn.close()

def selectSQL_getex(ex_info):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''SELECT *  from ex where address=%s''', (ex_info.address,))
    return cursor.fetchall()

# 删除180日前的数据
def DeleteSQL():
    if check_database(db):
        conn = initMySQL()
        cursor = conn.cursor()
        cursor.execute("delete from ex WHERE dDate < DATE_SUB(NOW(), INTERVAL 180 DAY);")  # 删除180日之前的数据
        conn.commit()
        cursor.close()
        conn.close()
