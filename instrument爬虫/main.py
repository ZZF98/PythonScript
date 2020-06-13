from urllib.request import urlopen

import pymysql
from bs4 import BeautifulSoup

# 设置代理
user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
]


# 连接函数
def connect_mysql():
    return pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="instrument",
                           charset="utf8", connect_timeout=30)


# 新增类型
def insert_category(data):
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
         INSERT INTO category (
         parent_id,
         name,
         level,
         url,
         lv) VALUES (
         %s,
         %s,
         %s,
         %s,
         %s);
         """
        try:
            # 执行SQL语句
            cursor.execute(sql, [data["parent_id"],
                                 data["name"],
                                 data["level"],
                                 data["url"],
                                 data["lv"],
                                 ])
            print(cursor.lastrowid)
            id = cursor.lastrowid
            # 提交事务
            conn.commit()
        except Exception as e:
            print(e)
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()
        return id


# 新增仪器
def insert_instrument(data):
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
         INSERT INTO instrument (
         name,
         price,
         brand,
         model,
         origin,
         category,
         pic_url,
         url) VALUES (
         %s,
         %s,
         %s,
         %s,
         %s,
         %s,
         %s,
         %s);
         """
        try:
            # 执行SQL语句
            cursor.execute(sql, [data["name"],
                                 data["price"],
                                 data["brand"],
                                 data["model"],
                                 data["origin"],
                                 data["category"],
                                 data["pic_url"],
                                 data["url"],
                                 ])
            print(cursor.lastrowid)
            id = cursor.lastrowid
            # 提交事务
            conn.commit()
        except Exception as e:
            print(e)
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()
        return id


# 获取一级节点
def get_level_one_category():
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
            name,
            url,
            level
        FROM
            category
            WHERE parent_id is NULL 
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


# 获取三级节点（未获取数据的那种）
def get_level_three_category():
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
            `name`,
            url 
        FROM
            category 
        WHERE
            lv = 3 
            AND STATUS IN ( 0, 2 )
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


# 更新level
def updata_level(id, level):
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
       UPDATE category SET level=%s WHERE id=%s
        """
        try:
            # 执行SQL语句
            cursor.execute(sql, [level,
                                 id])
            # 提交事务
            conn.commit()
        except Exception as e:
            print(e)
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()


# 更新仪器状态
def updata_category_status(id, status):
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
       UPDATE category SET status=%s WHERE id=%s
        """
        try:
            # 执行SQL语句
            cursor.execute(sql, [status, id])
            # 提交事务
            conn.commit()
        except Exception as e:
            print(e)
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()


# 获取所有种类
def get_all_classify():
    url = 'https://www.instrument.com.cn/'
    html = urlopen(url)
    bsObj = BeautifulSoup(html, fromEncoding="gb18030")
    for li in bsObj.select(".step1.fl.imClassbox ul li"):
        data = {}
        data["url"] = li.find("a")["href"]
        data["name"] = li.text.strip()
        data["level"] = ""
        data["parent_id"] = None
        data["lv"] = 1
        id = insert_category(data)
        updata_level(id, id)


# 创建子类信息(所有类别)
def create_subclass_data():
    for id, name, url, level in get_level_one_category():
        print(id, name, url)
        html = urlopen(url)
        bsObj = BeautifulSoup(html, fromEncoding="gb18030")
        for li in bsObj.select("#Classfiy .na-list.clearfix"):
            divs = li.find_all("div")
            # 创建二级类别
            try:
                div1 = BeautifulSoup(str(divs[0]), fromEncoding="gb18030")
            except Exception as e:
                print(e)
            else:
                a = div1.find("a")
                data = {}
                data["url"] = a["href"]
                data["name"] = a.text.strip()
                data["level"] = ""
                data["parent_id"] = id
                data["lv"] = 2
                i_id = insert_category(data)
                tow_level = level + "." + str(i_id)
                updata_level(i_id, tow_level)

                # 创建三级列表
                try:
                    div2 = BeautifulSoup(str(divs[2]), fromEncoding="gb18030")
                except Exception as e:
                    print(e)
                else:
                    for a in div2.select("a"):
                        data = {}
                        data["url"] = a["href"]
                        data["name"] = a.text.strip()
                        data["level"] = ""
                        data["parent_id"] = i_id
                        data["lv"] = 3
                        i_i_id = insert_category(data)
                        data["level"] = tow_level + "." + str(i_i_id)
                        updata_level(i_i_id, data["level"])


# 创建所有url列表
def create_url_list(url):
    url_list = []
    url_list.append(url)
    html = urlopen(url)
    bsObj = BeautifulSoup(html, fromEncoding="gb18030")
    aList = bsObj.select(".msdn a")[0:-1]
    for a in aList:
        s = url.split("/")
        s[-1] = a["href"]
        url_list.append('/'.join(s))
    return url_list


# 创建仪器数据
def create_instrument():
    for id, name, url in get_level_three_category():
        print(id, name, url)
        updata_category_status(id, 2)
        # 获取每页仪器数据并插入
        for u in create_url_list(url):
            print(u)
            html = urlopen(u)
            bsObj = BeautifulSoup(html, fromEncoding="gb18030")
            liList = bsObj.findAll("li", {"class": "mt10 mb10 clearfix alert_out liItemCompare"})
            for li in liList:
                data = {}
                data["pic_url"] = li.img["src"]
                data["category"] = id

                div = li.find("div", {"class", "se_pic_link1_con fl ml10"})
                data["name"] = div.h3.a["title"]
                data["url"] = div.h3.a["href"]

                data["price"] = "未知"
                data["brand"] = "未知"
                data["model"] = "未知"
                data["origin"] = "未知"

                table = li.find("table")
                trList = table.findAll("tr")
                for tr in trList:
                    tdList = tr.findAll("td")
                    for td in tdList:
                        if "品牌：" in td.text.strip():
                            data["brand"] = td.text.strip().split('：')[1]
                            continue
                        if "型号：" in td.text.strip():
                            data["model"] = td.text.strip().split('：')[1]
                            continue
                        if "产地：" in td.text.strip():
                            data["origin"] = td.text.strip().split('：')[1]
                            continue
                        if "参考报价：" in td.text.strip():
                            data["price"] = td.text.strip().split('：')[1].strip()
                            continue

                print(data)
                insert_instrument(data)
        # 更新状态
        updata_category_status(id, 1)


# 创建仪器数据
def create_instrument_two():
    for id, name, url in get_level_three_category():
        print(id, name, url)
        updata_category_status(id, 2)
        # 获取每页仪器数据并插入
        for u in create_url_list(url):
            print(u)
            html = urlopen(u)
            bsObj = BeautifulSoup(html, fromEncoding="gb18030")
            lis = bsObj.findAll("li", {"class": "p5 mb15 solidAll_gray2"})
            for li in lis:
                data = {}
                a = li.find("h3").a
                data["name"] = a.text
                data["url"] = a["href"]
                data["category"] = id
                try:
                    html = urlopen(a["href"])
                    detailObs = BeautifulSoup(html, fromEncoding="gb18030")
                except Exception as e:
                    print(e)
                else:
                    div = detailObs.find("div", {"class": "center1100 clearfix pr"})

                    try:
                        img = div.img
                    except Exception as e:
                        print(e)
                    else:
                        data["pic_url"] = img["src"]

                    data["price"] = "未知"
                    data["brand"] = "未知"
                    data["model"] = "未知"
                    data["origin"] = "未知"

                    try:
                        right = div.find("div", {"class": "_parameter clearfix"})
                    except Exception as e:
                        print(e)
                        continue
                    prSpan = right.find("div", {"class": "price pr"}).find("span", {"class": "_part"})
                    data["price"] = prSpan.text

                    rightLis = right.find("ul").findAll("li")
                    for rightLi in rightLis:
                        if "品牌" in rightLi.text:
                            data["brand"] = rightLi.text.split('品牌')[1].strip()
                            continue
                        if "型号" in rightLi.text: 'm'
                        data["model"] = rightLi.text.split('型号')[1].strip()
                        continue
                    if "产地" in rightLi.text:
                        data["origin"] = rightLi.text.split('产地')[1].strip()
                        continue
                print(data)
                insert_instrument(data)
    # 更新状态
    updata_category_status(id, 1)



