import pymysql


# 连接函数
def connect_mysql():
    return pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="instrument",
                           charset="utf8", connect_timeout=30)


def get_data():
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
            SELECT id,category FROM instrument
        """
        # 执行SQL语句
        cursor.execute(sql)
        # 获取结果
        res = cursor.fetchall()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return res


def get_category_name(id):
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
            SELECT `name`,id,level FROM category WHERE id=%s
        """
        # 执行SQL语句
        cursor.execute(sql, [id])
        # 获取结果
        res = cursor.fetchall()
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return res


# 更新level
def updata_data(id, category_name, category0, category1):
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
            UPDATE instrument SET category_name=%s, category_name_0=%s, category_name_1=%s WHERE id=%s
        """
        try:
            # 执行SQL语句
            cursor.execute(sql, [category_name,
                                 category0,
                                 category1,
                                 id])
            # 提交事务
            conn.commit()
        except Exception as e:
            print(e)
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()


for id, category in get_data():
    print(id, category)
    name = get_category_name(category)[0][0]
    level = get_category_name(category)[0][2]
    category0 = get_category_name(level.split('.')[0])[0][0]
    category1 = get_category_name(level.split('.')[1])[0][0]
    updata_data(id, name, category0, category1)
