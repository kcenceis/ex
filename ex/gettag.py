import Mysqldb
import content_page
from Utils import ex_info


def gettag(address):
    print('gettag:{}'.format(address))
    content_page.get_TAG_LIST(address)


def deletetag(address):
    print('deletetag:{}'.format(address))
    conn = Mysqldb.initMySQL()
    cursor = conn.cursor()
    cursor.execute('delete from push where address=%s', (address,))
    conn.commit()
    cursor.close()
    conn.close()


try:
    conn = Mysqldb.initMySQL()
    cursor = conn.cursor()
    cursor.execute('''SELECT address from push limit 1''')
    result = cursor.fetchone()
    conn.close()
    if len(result[0]) != 0:
        address = result[0]
        gettag(address)
        deletetag(address)
except:
    print()
