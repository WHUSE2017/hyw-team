#-*- coding:utf-8 -*-
import json
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def readFile():
    cpath = os.path.dirname(os.getcwd())  # 获取当前工作目录的上一级目录
    fpath = cpath + '/cache' + '/subscribe.json'
    if os.path.exists(fpath):  # 判断文件是否存在
        f = open(fpath)
        content = f.read()
        # 测试打印json文件内容
        # lists=json.loads(content)['list']
        # for i in lists:
        #     for k in i:
        #         print i[k]
        f.close()
        return content
    else:
        f = open(fpath, 'w')  # 不存在就新建一个
        f.close()
        return 0


def writeFile(content):
    cpath = os.path.dirname(os.getcwd())
    fpath = cpath + '/cache' + '/subscribe.json'
    f = open(fpath, 'w')
    f.write(content)
    f.close()


def updateSubscribeList(name, address, lastEpisode, updatetime):
    content = readFile()
    if content:
        subscribe_list = json.loads(content)
        lists = subscribe_list['list']
        for i in lists:
            if i['name'] == name:
                print 'the name is already in list'
                return
    else:
        subscribe_list = {
            'list': [],
            'total': 0
        }
    new_subscribe = {'name': name, 'address': address,
                     'lastEpisode': lastEpisode, 'updatetime': updatetime}
    subscribe_list['list'].append(new_subscribe)
    subscribe_list['total'] += 1
    writeFile(json.dumps(subscribe_list))


def deleateSubscribeList(name):
    content = readFile()
    if content:
        subscribe_list = json.loads(content)
    list = subscribe_list['list']
    index = 0
    for i in range(len(list)):
        if name in list[i]:
            index = i
    del list[index]
    subscribe_list['list'] = list
    subscribe_list['total'] -= 1
    writeFile(json.dumps(subscribe_list))


def getUrl():
    url = []
    content = readFile()
    subscribe_list = json.loads(content)
    list=subscribe_list['list']
    for i in list:
        url.append(i['address'])
    print type(url)
    return url


def updateLastEpisode(episodes):
    content = readFile()
    subscribe_list = json.loads(content)
    m = 0
    for i in subscribe_list['list']:
        i['lastEpisode'] = episodes[m]
        m += 1
    writeFile(json.dumps(subscribe_list))


# updateSubscribeList('abc','www.baidu.com',5,'Monday')
# deleateSubscribeList('abc')
