import logging
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Proxy
from selenium.webdriver.common.proxy import ProxyType

url = 'https://www.chemsrc.com/casindex/'
host = 'https://www.chemsrc.com'
# url页面列表
urlList = []
# url页面上的路径列表
urlDateList = ['https://www.chemsrc.com/cas/6222-55-5_46532.html', 'https://www.chemsrc.com/cas/5434-29-7_47643.html']
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


# proxyPool = ['1.197.204.251:9999', '1.198.72.8:9999']

# 获取代理
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()


# 删除
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


# 获取所有url数据
def getAllUrlDate(driver):
    rowCount = 1
    for urls in urlList:
        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        errcout = 0
        while True:
            try:
                # 删除代理并重新获取
                if errcout > 5:
                    print("删除代理" + headers["preProxy"])
                    delete_proxy(headers["preProxy"])
                    driver = getDriver()
                driver.get(urls)
                time.sleep(1)
                body = driver.find_element_by_tag_name("tbody").find_elements_by_class_name("rowDat")
                for row in body:
                    strs = row.find_elements_by_class_name("v-middle")[0].find_element_by_tag_name("a").get_attribute(
                        "href")
                    print(strs)
                    if strs not in urlDateList:
                        urlDateList.append(strs)
                break
            except:
                errcout += 1
                print("url:" + urls + "  错误次数:" + str(errcout))
        print(urlDateList)
        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        rowCount += 1
        time.sleep(1)


# 创建所有页面Url
def creatUrlDate(driver):
    # 获取页数
    errcout = 0
    while True:
        try:
            # 删除代理并重新获取
            if errcout > 5:
                print("删除代理" + headers["preProxy"])
                delete_proxy(headers["preProxy"])
                driver = getDriver()
            driver.get(url)
            time.sleep(1)
            el = driver.find_element_by_id("casIdxUl").find_elements_by_class_name("disabled")[-1]
        except:
            errcout += 1
            print("url:" + url + "  错误次数:" + str(errcout))
        else:
            print("一共:" + el.text)
            count = el.text[1:-1]
            for i in range(1, int(count) + 1):
                strUrl = url + str(i) + ".html"
                urlList.append(strUrl)
            break


# 获取driver对象
def getDriver():
    # 构建请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        headers
    )
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
    driver = webdriver.PhantomJS(executable_path='download/phantomjs.exe', desired_capabilities=dcap)
    return driver


def creatData(driver):
    rowCount = 1
    for urlDate in urlDateList:
        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        errcout = 0
        while True:
            try:
                # 删除代理并重新获取
                if errcout > 5:
                    driver.quit()
                    print("删除代理" + headers["preProxy"])
                    delete_proxy(headers["preProxy"])
                    driver = getDriver()
                    errcout = 0

                # 反爬虫
                driver.set_window_size(800, 800)
                driver.get(urlDate)
                time.sleep(1)
                # 获取图片url
                imgUrl = driver.find_element_by_id("structdiv").find_element_by_tag_name("img").get_attribute("src")
                tbodyTr = driver.find_element_by_id("baseTbl").find_element_by_tag_name(
                    "tbody").find_elements_by_tag_name("tr")
                # 常用名
                common_name = tbodyTr[0].find_elements_by_tag_name("td")[1].find_element_by_tag_name("a").text
                # 英文名
                english_name = tbodyTr[0].find_elements_by_tag_name("td")[2].find_element_by_tag_name("a").text
                # cas
                cas = tbodyTr[1].find_elements_by_tag_name("td")[0].find_element_by_tag_name("a").text
                # 分子量
                molecular_weight = tbodyTr[1].find_elements_by_tag_name("td")[1].text
                # 密度
                density = tbodyTr[2].find_elements_by_tag_name("td")[0].text
                # 沸点
                boiling_point = tbodyTr[2].find_elements_by_tag_name("td")[1].text
                # 分子式
                molecular_formula = tbodyTr[3].find_elements_by_tag_name("td")[0].text
                # 熔点
                melting_point = tbodyTr[3].find_elements_by_tag_name("td")[1].text
                # msds
                msds = tbodyTr[4].find_elements_by_tag_name("td")[0].text
                # 闪点
                flash_point = tbodyTr[4].find_elements_by_tag_name("td")[1].text
                print(common_name)
                print(english_name)
                print(cas)
                print(molecular_weight)
                print(density)
                print(boiling_point)
                print(molecular_formula)
                print(melting_point)
                print(msds)
                print(flash_point)
                print(imgUrl)


                break
            except:
                errcout += 1
                print("url:" + urlDate + "  错误次数:" + str(errcout))


def main():
    driver = getDriver()
    # 获取详细数据并新增
    creatData(driver)


if __name__ == '__main__':
    main()
