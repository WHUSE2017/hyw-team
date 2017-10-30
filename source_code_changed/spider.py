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
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    # chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
    # os.environ["webdriver.chrome.driver"] = chromedriver

    driver = webdriver.PhantomJS(
        executable_path="phantomjs.exe", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], desired_capabilities=dcap)
    # driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.get(address)
    return driver


def search_bilibili(content):
    raw_content = content
    content = Bilibili_replaceBlank(content)
    address = 'https://search.bilibili.com' + '/all?keyword=' + content
    driver = connection(address)
    # print driver.current_url
    try:
        element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[5]/div[3]/div/li/ul/a")))
        url = element1.get_attribute('href')
        print url
        element1.click()
    except:
        # driver.quit()
        search_iqiyi(driver, raw_content)
        return
    handles = driver.window_handles
    driver.switch_to_window(handles[1])
    print 1
    element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/ul")))
    try:
        if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]"):
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]").click()
            li_lists = driver.find_elements(By.CLASS_NAME, "v1-short-text")
        else:
            li_lists = driver.find_elements(By.CLASS_NAME, "v1-complete-text")
    except:
        li_lists=driver.find_elements(By.CLASS_NAME,"v1-complete-text")
        print li_lists
    updatetime = driver.find_element(
        By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/div[3]/em/span[2]")
    updatetime = updatetime.text.split(' ')[1]
    updateSubscribeList(raw_content, url, len(li_lists), updatetime)
    driver.quit()
    # print len(li_lists)
    # updateSubscribeList(raw_content, url, len(li_lists), updatetime)


def search_iqiyi(driver, content):
    raw_content = content
    content = iqiyi_replaceBlank(content)
    address = 'http://so.iqiyi.com/so' + '/q_' + content
    # driver = connection(address)
    driver.get(address)
    print driver.current_url
    # try:
    element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "body > div.page-search > div.container.clearfix > div.search_result_main > div > div.mod_search_result > div > ul > li:nth-child(1) > div > div.info_item.mt15 > div > div:nth-child(2) > ul:nth-child(1)")))
    li_list = element1.find_elements(By.CLASS_NAME, "album_link")
    # print len(li_list)
    updatetime = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[4]/div[1]/div/div[2]/div/ul/li[1]/div/div[1]/div/span").text
    updateSubscribeList(raw_content, driver.current_url,
                        len(li_list), updatetime)
    driver.quit()


def getLastEpisode(url):
    print url
    if not judgeSubscribeList():
        print 'the list is empty'
        return 
    episodes = []
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
    dcap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(
        executable_path="..\phantomjs.exe", service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], desired_capabilities=dcap)
    for i in range(len(url)):
        driver.get(url[i])
        print url[i]
        if 'bilibili' in url[i]:
            element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/div/div[3]/ul")))
            if driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]"):
                driver.find_element(
                    By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[1]/ul/li[2]").click()
                li_lists = driver.find_elements(By.CLASS_NAME, "v1-short-text")
            else:
                li_lists = driver.find_elements(
                    By.CLASS_NAME, "v1-complete-text")
        else:
            element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "body > div.page-search > div.container.clearfix > div.search_result_main > div > div.mod_search_result > div > ul > li:nth-child(1) > div > div.info_item.mt15 > div > div:nth-child(2) > ul:nth-child(1)")))
            li_lists = element1.find_elements(By.CLASS_NAME, "album_link")
        episodes.append(len(li_lists))
        print len(li_lists)
    updateLastEpisode(episodes)


if __name__ == '__main__':
    b_address = 'https://search.bilibili.com'
    i_address = 'http://so.iqiyi.com/so'
    content = u'宝石之国'
    search_bilibili(content)#现在直接调用这个函数就可以搜索B站和爱奇艺了
    # getLastEpisode(getUrl())  #抓取更新集数
    content = '十二大战'
    content = content.encode('utf-8')
    search_bilibili(content)#现在直接调用这个函数就可以搜索B站和爱奇艺了
    search_bilibili(u'黑色五叶草')