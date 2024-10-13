import mysql.connector
import json
import os
with open(os.path.split(os.path.realpath(__file__))[0]+os.sep+"config.json", "r") as f:
    result = json.loads(f.read())
    host = result['host']
    user = result['user']
    password = result['password']
    db = result['db']

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
        cursor.execute("CREATE DATABASE " + db)
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
       cosplayer            text,
       mixed                text,
       other                text,
       reclass              text,
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
        cursor.execute('''
         CREATE TABLE title_filter                      
        (id INT PRIMARY KEY AUTO_INCREMENT,
        tag              text,
        dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
        cursor.execute('''
         CREATE TABLE ex_gd3                      
        (id INT PRIMARY KEY AUTO_INCREMENT,
        address              text,
        gd3_uploader              text,
        gd3_uploader_url              text,
        gd3_Posted              text,
        gd3_Language              text,
        gd3_Length              text,
        dDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );''')
        cursor.execute("""
CREATE PROCEDURE `getEX`(IN `pageoffset` bigint, IN `pagecount` bigint)
begin
  # 局部变量声明必须在游标声明之前
  declare i int default 0;
-- 创建临时表
CREATE TEMPORARY TABLE temp_filter select * from filter_list;
CREATE TEMPORARY TABLE temp_title_filter select * from title_filter;
CREATE TEMPORARY TABLE temp_ex select a.*,b.gd3_uploader,b.gd3_uploader_url,b.gd3_Posted,b.gd3_Language,b.gd3_Length from ex as a inner join ex_gd3 as b where a.address = b.address and a._delete is NULL;
#CREATE TEMPORARY TABLE temp_ex select * from ex where _delete is NULL;
#CREATE TEMPORARY TABLE temp_ex_gd3 select * from ex_gd3;
-- 循环 获得filterlist中的过滤条件
SET @row_count = (SELECT COUNT(*) FROM temp_filter);
set @filter_list_tag = 'NOT category like \'%Western%\' AND NOT category like \'%Misc%\'  AND NOT category like \'%Non-H%\' ';
while i < @row_count DO
set @filter_list_tag= concat(@filter_list_tag,' ',(select CONCAT('AND NOT ',tag_list,' like \'%',tag,'%\'')   from temp_filter limit i,1));
set i = i +1;
END while;
SET @row_count = (SELECT COUNT(*) from title_filter);
SET i=0;
while i < @row_count DO
set @filter_list_tag= concat(@filter_list_tag,' ',(select CONCAT('AND NOT title like \'%',title,'%\'')   from title_filter limit i,1));
set i = i +1;
END while;

set @query = CONCAT('select * from (select * from temp_ex) as iz where ', @filter_list_tag,'  order by dDate desc LIMIT ', pageoffset,',',pagecount);
#set @query = CONCAT('select count(*) from (select * from temp_ex) as iz where ', @filter_list_tag,'  order by dDate desc ');
-- 
prepare statement from @query;
execute statement;
deallocate prepare statement;
-- 
DROP TEMPORARY TABLE IF EXISTS temp_title_filter;
DROP TEMPORARY TABLE IF EXISTS temp_filter;
DROP TEMPORARY TABLE IF EXISTS temp_extable;
DROP TEMPORARY TABLE IF EXISTS temp_ex;
end
        """)
        cursor.execute("""
CREATE PROCEDURE `getEX_Count` ()
begin
 # 获取EX数据数量
  # 局部变量声明必须在游标声明之前
  declare i int default 0;
-- 创建临时表
CREATE TEMPORARY TABLE temp_filter select * from filter_list;
CREATE TEMPORARY TABLE temp_title_filter select * from title_filter;
CREATE TEMPORARY TABLE temp_ex select a.*,b.gd3_uploader,b.gd3_uploader_url,b.gd3_Posted,b.gd3_Language,b.gd3_Length from ex as a inner join ex_gd3 as b where a.address = b.address and a._delete is NULL;
#CREATE TEMPORARY TABLE temp_ex select * from ex where _delete is NULL;
#CREATE TEMPORARY TABLE temp_ex_gd3 select * from ex_gd3;
-- 循环 获得filterlist中的过滤条件
SET @row_count = (SELECT COUNT(*) FROM temp_filter);
set @filter_list_tag = 'NOT category like \'%Western%\' AND NOT category like \'%Misc%\'  AND NOT category like \'%Non-H%\' ';
while i < @row_count DO
set @filter_list_tag= concat(@filter_list_tag,' ',(select CONCAT('AND NOT ',tag_list,' like \'%',tag,'%\'')   from temp_filter limit i,1));
set i = i +1;
END while;
SET @row_count = (SELECT COUNT(*) from title_filter);
SET i=0;
while i < @row_count DO
set @filter_list_tag= concat(@filter_list_tag,' ',(select CONCAT('AND NOT title like \'%',title,'%\'')   from title_filter limit i,1));
set i = i +1;
END while;


-- 拼接查询语句
set @query = CONCAT('select count(*) from (select * from temp_ex) as iz where ', @filter_list_tag);
-- 
prepare statement from @query;
execute statement;
deallocate prepare statement;
-- 
DROP TEMPORARY TABLE IF EXISTS temp_title_filter;
DROP TEMPORARY TABLE IF EXISTS temp_filter;
DROP TEMPORARY TABLE IF EXISTS temp_ex;
end;;
        """)

        cursor.execute("""
CREATE PROCEDURE `getid`(IN `ex_id` int)
begin
select a.language,a.parody,a._character,a._group,a.artist,a.male,a.female,a.misc,a.cosplayer,a.mixed,a.other,a.reclass,b.gd3_uploader
from ex as a 
inner join  ex_gd3 as b
where a.id=ex_id and a.address=b.address;
end
                """)
        mydb.commit()
        mydb.close()


def insertSQL(ex_info):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ex (title,address,torrent_address,magnet,file_name,category)  VALUES (%s,%s,%s,%s,%s,%s)",
        (
            ex_info.title,
            ex_info.address,
            ex_info.torrent_address,
            ex_info.magnet,
            ex_info.file_name,
            ex_info.category,))
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


def updateSQL_TAG(address, ex_tag_list):
    try:
        conn = initMySQL()
        cursor = conn.cursor()
        cursor.execute('''UPDATE ex
        SET  language=%s,parody=%s,_character=%s,_group=%s,artist=%s,male=%s,female=%s,misc=%s,cosplayer=%s,mixed=%s,other=%s,reclass=%s,data1=1
        where address = %s ''', (
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
            ex_tag_list.reclass,
            address,
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error Occurred: {e}")

def insertSQL_gd3(address,ex_gd3):
        try:
            conn = initMySQL()
            cursor = conn.cursor()
            cursor.execute("select count(*) from ex_gd3 where address = %s ",(address,))
            result = cursor.fetchone()
            if result[0]==0:
                cursor.execute(
                    "INSERT INTO ex_gd3 (address,gd3_uploader,gd3_uploader_url,gd3_Posted,gd3_Language,gd3_Length)  VALUES (%s,%s,%s,%s,%s,%s)",
                    (address, ex_gd3.uploader, ex_gd3.uploader_url, ex_gd3.Posted, ex_gd3.Language, ex_gd3.Length,))
            else:
                cursor.execute('''UPDATE ex_gd3
        SET gd3_uploader=%s,gd3_uploader_url=%s,gd3_Posted=%s,gd3_Language=%s,gd3_Length=%s
        where address = %s ''',
                               (ex_gd3.uploader, ex_gd3.uploader_url, ex_gd3.Posted, ex_gd3.Language, ex_gd3.Length,address,)
                               )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error Occurred: {e}")


def selectSQL_getex(ex_info):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''SELECT count(*)  from ex where address=%s''', (ex_info.address,))
    return cursor.fetchone()


def selectSQL_HAVETAG(ex_info):
    conn = initMySQL()
    cursor = conn.cursor()
    cursor.execute('''SELECT count(*)  from ex where address=%s and _delete is NULL and data1 is NULL''',
                   (ex_info.address,))
    return cursor.fetchone()


# 删除180日前的数据
def DeleteSQL():
    if check_database(db):
        conn = initMySQL()
        cursor = conn.cursor()
        cursor.execute("delete from ex WHERE dDate < DATE_SUB(NOW(), INTERVAL 180 DAY);")  # 删除180日之前的数据
        conn.commit()
        cursor.close()
        conn.close()
