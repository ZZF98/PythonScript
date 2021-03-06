import logging
import random
import time

import pymysql as pymysql
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Proxy
from selenium.webdriver.common.proxy import ProxyType

url = 'https://www.chemsrc.com/casindex/'
host = 'https://www.chemsrc.com'
# url页面列表
urlList = []
# url页面上的路径列表
urlDateList = []
# 代理列表
proxyList = []
retriesCount = 3
logger = logging.getLogger(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Cookie': 'JSESSIONID=FC93CDD81B4B6A7A0E546FFCFC9E2763;'
              'ga=GA1.2.1861924803.1568266045;'
              'gid=GA1.2.140102893.1568266045;'
              'Hm_lvt_f121c3ffd570499b9229f30828cb0d5f=1568259831;'
              'Hm_lpvt_f121c3ffd570499b9229f30828cb0d5f=1568266077',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-User': '?1',
    'preProxy': '119.179.161.126:8060'
}

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
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


# proxyPool = ['1.197.204.251:9999', '1.198.72.8:9999']

# 获取代理
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


# 删除
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# 连接函数
def connect():
    return pymysql.connect(host="localhost", port=3306, user="root", passwd="12345678", db="chemsrc",
                           charset="utf8", connect_timeout=30)


# 新增url
def insertUrl(url):
    # 连接database
    try:
        conn = connect()
    except:
        logger.error("连接异常。。。。")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = "INSERT INTO chemsrc_url (url) VALUES (%s);"
        try:
            # 执行SQL语句
            cursor.execute(sql, [url])
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
        else:
            urlDateList.remove(url)
        cursor.close()
        conn.close()


# 新增Data
def insertData(id, data):
    # 连接database
    try:
        conn = connect()
    except:
        logger.error("连接异常。。。。")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = """
        INSERT INTO data (
        id,
        img_url,
        common_name,
        english_name,
        cas,
        molecular_weight,
        density,
        boiling_point,
        molecular_formula,
        melting_point,
        msds,
        flash_point
        ) VALUES (
        %s,
        %s,
        %s,
        %s,
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
            cursor.execute(sql, [id,
                                 data["img_url"],
                                 data["common_name"],
                                 data["english_name"],
                                 data["cas"],
                                 data["molecular_weight"],
                                 data["density"],
                                 data["boiling_point"],
                                 data["molecular_formula"],
                                 data["melting_point"],
                                 data["msds"],
                                 data["flash_point"]])
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
        else:
            updataUrl(id)
        cursor.close()
        conn.close()


# 新增Data
def insertDetailData(data):
    # 连接database
    try:
        conn = connect()
    except:
        logger.error("连接异常。。。。")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = """
        INSERT INTO detail_data (
        url,
        common_name,
        english_name,
        cas,
        molecular_weight,
        density,
        boiling_point,
        molecular_formula,
        melting_point,
        row_count
        ) VALUES (
        %s,
        %s,
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
            cursor.execute(sql, [
                data["url"],
                data["common_name"],
                data["english_name"],
                data["cas"],
                data["molecular_weight"],
                data["density"],
                data["boiling_point"],
                data["molecular_formula"],
                data["melting_point"],
                data["row_count"]])
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
        cursor.close()
        conn.close()


# 更新状态
def updataUrl(id):
    # 连接database
    try:
        conn = connect()
    except:
        logger.error("连接异常。。。。")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = """
          UPDATE chemsrc_url SET status=1 WHERE id=%s
          """
        try:
            # 执行SQL语句
            cursor.execute(sql, [id])
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
        else:
            cursor.close()
            conn.close()


# 获取分页数据
def getUrl(page):
    # 连接database
    try:
        conn = connect()
    except:
        logger.error("连接异常。。。。")
    else:
        # 定义要执行的SQL语句
        cursor = conn.cursor()
        # 修改数据的SQL语句
        sql = """
          SELECT id,url FROM chemsrc_url WHERE `status`='0' LIMIT %s,100
          """
        try:
            # 执行SQL语句
            cursor.execute(sql, (page - 1) * 100)
            # 提交事务
            conn.commit()
        except Exception as e:
            # 有异常，回滚事务
            conn.rollback()
        else:
            cursor.close()
            conn.close()
            return cursor.fetchall()


# 获取所有url数据
def getAllUrlDate(driver, rowCounts):
    rowCount = int(rowCounts)
    for urls in urlList:
        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        errcout = 0
        data = {}
        while True:
            try:
                # 删除代理并重新获取
                if errcout >= retriesCount:
                    # driver.service.process.send_signal(signal.SIGTERM)  # kill the specific phantomjs child proc
                    try:
                        print("删除代理" + headers["preProxy"])
                        delete_proxy(headers["preProxy"])
                    except:
                        pass
                    delete_proxy(headers["preProxy"])
                    driver = getDriver_proxy()
                    errcout = 0

                driver.get(urls)
                time.sleep(1)
                body = driver.find_element_by_tag_name("tbody").find_elements_by_class_name("rowDat")
                for row in body:
                    # 详情地址
                    urlDetail = row.find_elements_by_class_name("v-middle")[0].find_element_by_tag_name(
                        "a").get_attribute(
                        "href")
                    data["url"] = urlDetail
                    print(urlDetail)
                    # 中文名
                    common_name = row.find_elements_by_tag_name("td")[0].find_element_by_tag_name("a").text
                    data["common_name"] = common_name
                    print(common_name)
                    # 英文名
                    english_name = row.find_elements_by_tag_name("td")[1].text
                    data["english_name"] = english_name
                    print(english_name)
                    textList = str(row.find_elements_by_tag_name("td")[2].text).split('\n')
                    # 分子量
                    molecular_weight = textList[0].split("：")[1]
                    data["molecular_weight"] = molecular_weight
                    print(molecular_weight)
                    # 密度
                    density = textList[1].split("：")[1]
                    data["density"] = density
                    print(density)
                    # 沸点
                    boiling_point = textList[2].split("：")[1]
                    data["boiling_point"] = boiling_point
                    print(boiling_point)
                    # 熔点
                    melting_point = textList[3].split("：")[1]
                    data["melting_point"] = melting_point
                    print(melting_point)
                    # cas
                    cas = row.find_elements_by_tag_name("td")[3].find_element_by_tag_name("a").text
                    data["cas"] = cas
                    print(cas)
                    # 分子式
                    molecular_formula = row.find_elements_by_tag_name("td")[4].text
                    data["molecular_formula"] = molecular_formula
                    print(molecular_formula)
                    data["row_count"] = rowCount
                    insertDetailData(data)
                    if headers["preProxy"] not in proxyList:
                        proxyList.append(headers["preProxy"])
                        f1 = open('ip.txt', 'a')
                        for ip in proxyList:
                            f1.write(ip + "\n")
                        f1.close()
                break
            except:
                errcout += 1
                print("url:" + urls + "  错误次数:" + str(errcout) + "  页数为:" + str(rowCount))
        print(urlDateList)

        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        rowCount += 1
        time.sleep(1)


# 创建所有页面Url
def creatUrlDate(start, end):
    # 获取页数
    for i in range(start, end + 1):
        strUrl = url + str(i) + ".html"
        urlList.append(strUrl)


# 获取driver对象
def getDriver():
    # 构建请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        headers
    )
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    headers["preProxy"] = get_proxy().get("proxy")
    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': headers["preProxy"]
            # 'httpProxy': proxyPool[random.randint(0,
            #                                       len(proxyPool) - 1)]  # 代理ip和端口
        }
    )
    # 把代理ip加入到技能中
    # proxy.add_to_capabilities(dcap)
    driver = webdriver.PhantomJS(executable_path='download/phantomjs.exe', desired_capabilities=dcap)
    # 隐式等待5秒，可以自己调节
    # driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(3)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(3)
    return driver


# 获取driver对象（代理方式）
def getDriver_proxy():
    # 构建请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        headers
    )
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    headers["preProxy"] = get_proxy().get("proxy")
    proxy = Proxy(
        {
            'proxyType': ProxyType.MANUAL,
            'httpProxy': headers["preProxy"]
            # 'httpProxy': proxyPool[random.randint(0,
            #                                       len(proxyPool) - 1)]  # 代理ip和端口
        }
    )
    # 把代理ip加入到技能中
    proxy.add_to_capabilities(dcap)
    driver = webdriver.PhantomJS(executable_path='download/phantomjs2.exe', desired_capabilities=dcap)
    # 隐式等待5秒，可以自己调节
    # driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(3)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(3)
    # 反爬虫
    driver.set_window_size(800, 800)
    return driver


def main():
    driver = getDriver_proxy()
    # 1获取所有url
    creatUrlDate(22, 4411)
    # 获取所有url下的url详情列表
    getAllUrlDate(driver, 22)
    # 判断是否为空，
    # while True:
    #     if urlDateList:
    #         print(urlDateList)
    #     else:
    #         break
    #     for urlDate in urlDateList:
    #         insertUrl(urlDate)
    # # 2获取详细数据
    # page = input("input:")
    # # page = 1
    # while True:
    #     urlDateList = getUrl(int(page))
    #     if urlDateList:
    #         # page += 1
    #         print(urlDateList)
    #         creatData(driver, urlDateList)
    #     else:
    #         break


if __name__ == '__main__':
    main()

# def creatData(driver, urlDateList):
#     for urlDate in urlDateList:
#         print("---------------------------" + str(urlDate[0]) + "------------------------------------------------")
#         errcout = 0
#         data = {}
#         while True:
#             try:
#                 # 删除代理并重新获取
#                 if errcout >= retriesCount:
#                     driver.quit()
#                     try:
#                         print("删除代理" + headers["preProxy"])
#                         delete_proxy(headers["preProxy"])
#                     except:
#                         pass
#                     driver = getDriver()
#                     errcout = 0
#
#                 # 反爬虫
#                 driver.set_window_size(800, 800)
#                 driver.get(urlDate[1])
#                 time.sleep(1)
#                 try:
#                     tbodyTr = driver.find_element_by_id("baseTbl").find_element_by_tag_name(
#                         "tbody").find_elements_by_tag_name("tr")
#                 except:
#                     alt = driver.find_element_by_class_name("thumbnail").find_element_by_tag_name("img").get_attribute(
#                         "alt")
#                     if alt == '404 error':
#                         break
#                 # 获取图片url
#                 img_url = driver.find_element_by_id("structdiv").find_element_by_tag_name("img").get_attribute("src")
#                 data["img_url"] = img_url
#                 print(img_url)
#                 # 常用名
#                 try:
#                     common_name = tbodyTr[0].find_elements_by_tag_name("td")[1].find_element_by_tag_name("a").text
#                 except:
#                     common_name = tbodyTr[0].find_elements_by_tag_name("td")[1].text
#                 data["common_name"] = common_name
#                 print(common_name)
#                 # 英文名
#                 try:
#                     english_name = tbodyTr[0].find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").text
#                 except:
#                     english_name = tbodyTr[0].find_elements_by_tag_name("td")[2].text
#                 data["english_name"] = english_name
#                 print(english_name)
#                 # cas
#                 cas = tbodyTr[1].find_elements_by_tag_name("td")[0].find_element_by_tag_name("a").text
#                 data["cas"] = cas
#                 print(cas)
#                 # 分子量
#                 molecular_weight = tbodyTr[1].find_elements_by_tag_name("td")[1].text
#                 data["molecular_weight"] = molecular_weight
#                 print(molecular_weight)
#                 # 密度
#                 density = tbodyTr[2].find_elements_by_tag_name("td")[0].text
#                 data["density"] = density
#                 print(density)
#                 # 沸点
#                 boiling_point = tbodyTr[2].find_elements_by_tag_name("td")[1].text
#                 data["boiling_point"] = boiling_point
#                 print(boiling_point)
#                 # 分子式
#                 molecular_formula = tbodyTr[3].find_elements_by_tag_name("td")[0].text
#                 data["molecular_formula"] = molecular_formula
#                 print(molecular_formula)
#                 # 熔点
#                 melting_point = tbodyTr[3].find_elements_by_tag_name("td")[1].text
#                 data["melting_point"] = melting_point
#                 print(melting_point)
#                 # msds
#                 msds = tbodyTr[4].find_elements_by_tag_name("td")[0].text
#                 data["msds"] = msds
#                 print(msds)
#                 # 闪点
#                 flash_point = tbodyTr[4].find_elements_by_tag_name("td")[1].text
#                 data["flash_point"] = flash_point
#                 print(flash_point)
#                 insertData(urlDate[0], data)
#                 if headers["preProxy"] not in proxyList:
#                     proxyList.append(headers["preProxy"])
#                     f1 = open('ip.txt', 'a')
#                     for ip in proxyList:
#                         f1.write(ip + "\n")
#                     f1.close()
#                 break
#             except:
#                 errcout += 1
#                 print("url:" + urlDate[1] + "  错误次数:" + str(errcout))
