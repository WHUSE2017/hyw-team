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
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def Bilibili_replaceBlank(str):
    str = str.split(' ')
    for i in range(len(str)):
        str[i] = urllib.quote(str[i].encode('utf-8'))
    return '+'.join(str)


def iqiyi_replaceBlank(str):
    str = str.split(' ')
    for i in range(len(str)):
        str[i] = urllib.quote(str[i].encode('utf-8'))
    return '%20'.join(str)


def connection(address):
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
    # 不载入图片，爬页面速度会快很多
    # dcap["phantomjs.page.settings.loadImages"] = False
    chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver

    # driver = webdriver.PhantomJS(
    #     executable_path=".\phantomjs.exe", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], desired_capabilities=dcap)
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.get(address)
    return driver


def search_bilibili(address, content):
    content = Bilibili_replaceBlank(content)
    address = address + '/all?keyword=' + content
    driver = connection(address)
    print driver.current_url
    try:
        element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div[3]/div/li/ul/a")))
        element1.click()
    except:
        driver.quit()
        return 0
    handles = driver.window_handles
    driver.switch_to_window(handles[1])
    try:
        element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/ul")))
        if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]"):
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]").click()
            li_lists = driver.find_elements(By.CLASS_NAME, "v1-short-text")
        else:
            li_lists = driver.find_elements(By.CLASS_NAME, "v1-complete-text")
    except:
    	driver.quit()
    print len(li_lists)
    driver.quit()


def search_iqiyi(address, content):
    content = iqiyi_replaceBlank(content)
    address = address + '/q_' + content
    driver = connection(address)
    element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "body > div.page-search > div.container.clearfix > div.search_result_main > div > div.mod_search_result > div > ul > li:nth-child(1) > div > div.info_item.mt15 > div > div:nth-child(2) > ul:nth-child(1)")))
    li_list = element1.find_elements(By.CLASS_NAME, "album_link")
    print len(li_list)
    driver.quit()


if __name__ == '__main__':
    b_address = 'https://search.bilibili.com'
    i_address = 'http://so.iqiyi.com/so'
    content = u'狐妖小红娘'
    # search(address, content)
    # search_iqiyi(i_address, content)
    search_bilibili(b_address, content)
