# 刷csdn的访问量
import datetime
import logging
import random
import re
import time
from urllib import request
from urllib.request import urlopen

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
# https://www.kuaidaili.com/free/
request.ProxyHandler({"http": "114.234.83.42:9000", "http": "114.235.23.100:9000"})
proxies = {
    "http": "http://114.234.83.42:9000",
    "http": "http://114.235.23.100:9000",
}
# r=requests.get("http://youtube.com", proxies=proxies)

headers = {
    'User-Agent': ''
}

lists = []

# csdn用户
csdnUser = '/qq_37598011'
# https://blog.csdn.net/weixin_44727140
# 地址
url = 'https://blog.csdn.net' + csdnUser

# 游览数总数
sum = 2000000


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


def main(url, lists, sum):
    title = getTiltleNumber(url)
    if title > sum:
        print("已经达到访问量：" + title)
    else:
        last = 0
        i = 1
        while True:
            newUrl = url + "/article/list/" + str(i)
            getAllLink(newUrl, lists)
            if last == len(lists):
                break
            else:
                i += 1
                last = len(lists)
        urlList = list(set(lists))
        count = 0
        while title <= sum:
            count += 1
            randomUrl = urlList[random.randint(0,
                                               len(urlList) - 1)]
            headers["User-Agent"] = random.choice(user_agent_list)
            # request.build_opener(proxies)
            req = request.Request(randomUrl, headers=headers, method='GET')
            # 代理
            # req = requests.get(randomUrl, allow_redirects=False, headers=headers, proxies=proxies)
            html = urlopen(req)
            print("---------------------------" + str(count) + "------------------------------------------------")
            bsObj = BeautifulSoup(html)
            print(bsObj)
            print("----------------------------------------------------------------------------")
            if count % 100 == 0:
                title = getTiltleNumber(url)


def main2(url, lists, sum):
    driver = webdriver.PhantomJS(executable_path='download/phantomjs.exe')
    driver.get(url)
    time.sleep(1)
    try:
        pageNumber = driver.find_elements_by_class_name("ui-pager")
        title = int(driver.find_element(By.CLASS_NAME, "grade-box,clearfix").find_elements(By.TAG_NAME, "dl")[
                        -3].find_element(By.TAG_NAME, "dd").get_attribute("title"))
    except:
        pageNumber = []

    if pageNumber == []:
        pageNumber = 1
    else:
        pageNumber = pageNumber[-3].text

    for i in range(1, int(pageNumber) + 1):
        newUrl = url + "/article/list/" + str(i)
        getAllLink(newUrl, lists)

    urlList = list(set(lists))
    count = 0
    while title <= sum:
        count += 1
        randomUrl = urlList[random.randint(0,
                                           len(urlList) - 1)]
        headers["User-Agent"] = random.choice(user_agent_list)
        req = request.Request(randomUrl, headers=headers, method='GET')
        # 代理
        # req = requests.get(randomUrl, allow_redirects=False, headers=headers, proxies=proxies)
        html = urlopen(req)
        print("---------------------------" + str(count) + "------------------------------------------------")
        bsObj = BeautifulSoup(html)
        print(bsObj)
        print("----------------------------------------------------------------------------")
        if count % 100 == 0:
            title = getTiltleNumber(url)


if __name__ == '__main__':
    # 方式一：
    main(url, lists, sum)
    # main2(url, lists, sum)
    # 下载百度
    # request.urlretrieve("http://www.baidu.com", "index.html")
    # parameter = {"wd": "猪"}
    #
    # url = "http://www.baidu.com/s?" + parse.urlencode(parameter)
    # req = urlopen(url)
    # print(BeautifulSoup(req))
    # encode = parse.urlencode(parameter)
    # qs = parse.parse_qs(encode)
    # print(qs)
