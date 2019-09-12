import logging
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

url = 'https://www.chemsrc.com/casindex/'
urlList = []
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
    'Sec-Fetch-User': '?1'

}


def getAllUrlDate(driver):
    rowCount = 1
    for urls in urlList:
        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        while True:
            try:
                driver.get(urls)
                time.sleep(1)

            except:
                print("重试")

        print("---------------------------" + str(rowCount) + "------------------------------------------------")
        rowCount += 1
        time.sleep(1)


def creatUrlDate(driver):
    # 获取页数
    driver.get(url)
    time.sleep(1)
    el = driver.find_element_by_id("casIdxUl").find_elements_by_class_name("disabled")[-1]
    print("一共:" + el.text)
    count = el.text[1:-1]
    for i in range(1, int(count) + 1):
        strUrl = url + str(i) + ".html"
        urlList.append(strUrl)


def main():
    # 构建请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        headers
    )
    driver = webdriver.PhantomJS(executable_path='download/phantomjs.exe', desired_capabilities=dcap)
    # 获取所有url
    creatUrlDate(driver)
    # 获取所有url下的url详情列表
    getAllUrlDate(driver)


if __name__ == '__main__':
    main()
