#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import urllib
import time
import os
from handleJson import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

SOURCEMAP = {'iqiyi': '爱奇艺', 'bilibili': 'B站', 'dilidili': 'D站', 'youku': '优酷'}


def iqiyi_replaceBlank(str):
    str = str.split(' ')
    for i in range(len(str)):
        str[i] = urllib.quote(str[i].encode('utf-8'))
    return '%20'.join(str)


def connection(address):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    # chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = chromedriver

    driver = webdriver.PhantomJS(
        executable_path="..\phantomjs.exe", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], desired_capabilities=dcap)
    # driver = webdriver.Chrome(chromedriver)
    # driver.maximize_window()
    driver.get(address)
    return driver


def search_aiqiyi(content):
    if content=='':
        address='http://m.iqiyi.com/search.html'
        driver=connection(address)
        return driver
    else:
        raw_content = content
        content = iqiyi_replaceBlank(content)
        address = 'http://m.iqiyi.com/search.html?source=input&vfrm=2-3-0-1&key=' + content
        driver = connection(address)
        try:
            element1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m-search-number")))
            return driver
        except:
            print 'have no results'
            driver.quit()
            return 0


def get_info(driver):
    if driver == 0:
        return
    raw_source = driver.find_element(By.CLASS_NAME, "icon-videoSource")
    source = raw_source.get_attribute('class').split(' ')[1].split('-')[2]
    if SOURCEMAP.has_key(source):
        sourcename = SOURCEMAP[source]
    else:
        print 'have no sourcename'
    print sourcename
    return sourcename


def get_lastEpisode(driver):
    episodes = driver.find_elements(By.CLASS_NAME, "c-album-item")
    last = episodes[4].get_attribute('data-widget-ptype').split('-')[-1]
    address = episodes[4].get_attribute('href')
    print last
    return (int(last), address)


def add_list(name):
    raw_content = readFile()
    content = json.loads(raw_content)
    driver=search_aiqiyi(name)
    sourcename=get_info(driver)
    last,address=get_lastEpisode(driver)
    updateSubscribeList(name,address,last,sourcename)
    driver.quit()


def Update():
    raw_content = readFile()
    content = json.loads(raw_content)
    subscribe_list = content['list']
    driver=search_aiqiyi('')
    search_input=driver.find_element(By.CLASS_NAME,"search-input")
    search_btn=driver.find_element(By.CSS_SELECTOR,"#headerEl > div > div.header-search-box > div.header-searchBtn > a")
    for i in subscribe_list:
        search_input.clear()
        search_input.send_keys(i['name'])
        search_btn.click()
        i['last'], i['address'] = get_lastEpisode(driver)
    content['list'] = subscribe_list
    writeFile(json.dumps(content))
    driver.quit()


# getinfo(u'银魂走光篇')
# get_lastEpisode(search_aiqiyi(u'银魂走光篇'))
# add_list(u'奇诺之旅 新作')
Update()
