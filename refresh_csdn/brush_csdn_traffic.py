# 刷csdn的访问量
import datetime
import logging
import random
import re
import time
from urllib import request
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType, Proxy

logger = logging.getLogger(__name__)

random.seed(datetime.datetime.now())
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
# https://www.kuaidaili.com/free/
request.ProxyHandler({"http": "114.234.83.42:9000", "http": "114.235.23.100:9000"})
proxies = {
    "http": "http://114.234.83.42:9000",
    "http": "http://114.235.23.100:9000",
}
# r=requests.get("http://youtube.com", proxies=proxies)

headers = {
    'User-Agent': '',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Host': 'blog.csdn.net',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-User': '?1',
    'Cookie': 'uuid_tt_dd=10_21050979110-1561947641260-125423; UN=qq_37598011; __yadk_uid=8weVoUulkpybMVDR3Or7muTFgvIiieui; _ga=GA1.2.1400725604.1562050604; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_21050979110-1561947641260-125423!5744*1*qq_37598011!1788*1*PC_VC; smidV2=20190703184407d5503dd016f76b59ae2db3ccb323a4ee0075bbcaa2ae7b150; dc_session_id=10_1563416655008.833988; Hm_ct_e5ef47b9f471504959267fd614d579cd=5744*1*qq_37598011!6525*1*10_21050979110-1561947641260-125423; acw_tc=2760820615674888479196583ee79cbe9614046097b622ea9660bc8fb78c07; UserName=qq_37598011; UserInfo=2dbade0627c245fcb8e069e61914229a; UserToken=2dbade0627c245fcb8e069e61914229a; UserNick=%E8%9B%87%E7%9A%AE%E7%9A%AE%E8%9B%8B; AU=754; BT=1567580608191; p_uid=U000000; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1567043028,1567043308,1567504544,1569036759; hasSub=true; aliyun_webUmidToken=T778F639477167CD7CB9BEE5C8C3C18B08B52DC11E8B242BF6F6F687788; acw_sc__v2=5d8d5fcd64dac2afd053e51c846b3b57951854d2; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1569490177,1569490237,1569490331,1569546248; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FarticleList%252Flist%22%2C%22tid%22%3A%22f6d1c325e27d64%22%2C%22q%22%3A0%2C%22a%22%3A94%7D; dc_tos=pygugx; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1569547330'
}

lists = []

# csdn用户
csdnUser = '/qq_37598011'
# https://blog.csdn.net/weixin_44727140
# 地址
url = 'https://blog.csdn.net' + csdnUser

# 游览数总数
sum = 2000000
proxy = ''


# 获取代理
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


# 删除
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# 获取页面所有文章的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 找出所有以"http"或"www"开头且不包含当前URL的链接,/qq_37598011
    # for link in bsObj.findAll("a",
    #                           href=re.compile("^(http|www|https)((?!" + excludeUrl + ").)*$")):
    for link in bsObj.findAll("a",
                              href=re.compile(
                                  "^(http|www|https)://" + excludeUrl + "" + csdnUser + "(/article/details/|/article/list/)([0-9]*)$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


# 获取地址
def splitAddress(address):
    if "https://" in address:
        addressParts = address.replace("https://", "").split("/")
    else:
        addressParts = address.replace("http://", "").split("/")
    return addressParts


# 获取所有连接
def getAllLink(startingPage, lists):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    for a in externalLinks:
        if a not in lists:
            lists.append(a)


# 获取浏览数
def getTiltleNumber(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    obs = bsObj.find("div", {"class": "grade-box clearfix"})
    for child in obs.children:
        if child != '\n':
            if "title" in child.dd.attrs and "访问" in child.dt.string:
                return int(child.dd["title"])


def getChrome():
    chromeOptions = webdriver.ChromeOptions()
    proxy = get_proxy()["proxy"]
    print(proxy)
    # 禁止加载图片
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    chromeOptions.add_experimental_option('prefs', prefs)
    chromeOptions.add_argument("--proxy-server={}".format('27.152.91.37:9999'))
    driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=chromeOptions)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(3)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(3)
    return driver


def main(url, lists, sum):
    while True:
        try:
            # chrome://version/
            # http://npm.taobao.org/mirrors/chromedriver/
            # http://chromedriver.storage.googleapis.com/index.html
            # https://www.zdaye.com/FreeIPList.html
            # https://selenium-python-zh.readthedocs.io/en/latest/api.html
            driver = getChrome()
            driver.get("http://httpbin.org/get")
            print(driver.page_source)
            driver.get(url)

            pageNumber = driver.find_elements_by_class_name("ui-pager")
            title = int(driver.find_element(By.CLASS_NAME, "grade-box,clearfix").find_elements(By.TAG_NAME, "dl")[
                            -3].find_element(By.TAG_NAME, "dd").get_attribute("title"))
            print(title)

            if pageNumber == []:
                pageNumber = 1
            else:
                pageNumber = pageNumber[-3].text

            for i in range(1, int(pageNumber) + 1):
                newUrl = url + "/article/list/" + str(i)
                getAllLink(newUrl, lists)

            urlList = list(set(lists))
            count = 0
            errcout = 0
            while title <= sum:
                count += 1
                randomUrl = urlList[random.randint(0,
                                                   len(urlList) - 1)]
                try:
                    driver.get(randomUrl)
                    print(
                        "---------------------------" + str(
                            count) + "------------------------------------------------")
                    print(driver.find_element_by_class_name("title-article").text)
                    bsObj = driver.page_source
                    print(bsObj)
                    print("----------------------------------------------------------------------------")
                    if count % 100 == 0:
                        title = getTiltleNumber(url)
                except Exception as e:
                    print(e)
                    count = count - 1
                    errcout = errcout + 1
                    if errcout > 5:
                        driver.quit()
                        driver = getChrome()
                    pass
        except Exception as e:
            print(e)
            driver.quit()
            pass


if __name__ == '__main__':
    main(url, lists, sum)