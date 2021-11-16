import pymysql
loginInfo = {
    'host': '10.2.16.174',
    'port': 3306,
    'user': 'tfb1031_08',
    'passwd': '12171712',
    'db': 'test',
    'charset': 'utf8mb4'
}


def connect_to_tfb1031():
    conn = pymysql.connect(**loginInfo)
    cursor = conn.cursor()
    return conn, cursor

def disconnect(gfgfg):
    print('Close Connection MySQL')
    conn, cursor = connect_to_tfb1031()
    conn.close()

def insert_data_into_mysql(user_id, data):
    conn, cursor = connect_to_tfb1031()

    mysql_insert_query = f"""INSERT INTO Line_bot_info
                           VALUES ("{user_id}", %s, %s, %s); """
    cursor = conn.cursor()
    cursor.execute(mysql_insert_query, tuple(data))
    conn.commit()

def read_data_from_mysql(user_id):
    conn, cursor = connect_to_tfb1031()
    mysql_insert_query = """SELECT * FROM Line_bot_info;"""
    cursor.execute(mysql_insert_query)
    data_from_mysql = cursor.fetchall()



