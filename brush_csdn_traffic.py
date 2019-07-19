import datetime
import logging
import random
import re
from urllib import request
from urllib.request import urlopen

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

random.seed(datetime.datetime.now())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
}

lists = []

# csdn用户
csdnUser = '/qq_37598011'

# 地址
url = 'https://blog.csdn.net' + csdnUser

# 游览数总数
sum = 100000


# 获取页面所有外链的列表
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


def splitAddress(address):
    if "https://" in address:
        addressParts = address.replace("https://", "").split("/")
    else:
        addressParts = address.replace("http://", "").split("/")
    return addressParts


def getRandomExternalLink(startingPage, lists):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    for a in externalLinks:
        lists.append(a)


def getTiltle(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    obs = bsObj.find("div", {"class": "grade-box clearfix"})
    for child in obs.children:
        if child != '\n':
            if "title" in child.dd.attrs and "访问" in child.dt.string:
                return int(child.dd["title"])


def main(url, lists, sum):
    title = getTiltle(url)
    if title > sum:
        print("已经达到访问量：" + title)
    else:
        for i in range(1, 9):
            newUrl = url + "/article/list/" + str(i)
            getRandomExternalLink(newUrl, lists)
        urlList = list(set(lists))
        count = 0
        while title <= sum:
            count += 1
            randomUrl = urlList[random.randint(0,
                                               len(urlList) - 1)]
            req = request.Request(randomUrl, headers=headers, method='GET')
            html = urlopen(req)
            print("---------------------------" + str(count) + "------------------------------------------------")
            bsObj = BeautifulSoup(html)
            print(bsObj)
            print("----------------------------------------------------------------------------")
            if count % 100 == 0:
                title = getTiltle(url)


main(url, lists, sum)
