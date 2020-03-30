import pymysql


# 连接函数
def connect_mysql():
    return pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="instrument",
                           charset="utf8", connect_timeout=30)


# 获取一级节点
def get_data(parent_id):
    # 连接database
    try:
        conn = connect_mysql()
    except:
        print("连接异常")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = """
        SELECT
            id,
            name
        FROM
            category
            WHERE parent_id =%s
        """
        # 执行SQL语句
        cursor.execute(sql, [parent_id])
        # 获取结果
        res = cursor.fetchall()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return res


for id, name in get_data(0):
    print(name)
    for id_two, name_two in get_data(id):
        print("    " + name_two)
        for id_three, name_three in get_data(id_two):
            print("        " + name_three)
