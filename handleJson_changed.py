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
        subscribe_list = {
            'list': [],
            'total': 0
        }
        f.write(json.dumps(subscribe_list))
        f.close()
        return json.dumps(subscribe_list)


def writeFile(content):
    cpath = os.path.dirname(os.getcwd())
    fpath = cpath + '/cache' + '/subscribe.json'
    f = open(fpath, 'w')
    f.write(content)
    f.close()


def judgeSubscribeList():
    content = readFile()
    total = json.loads(content)['total']
    if total == 0:
        return False
    else:
        return True


def updateSubscribeList(name, address, lastEpisode, sourceName):
    content = readFile()
    subscribe_list = json.loads(content)
    lists = subscribe_list['list']
    for i in lists:
        if i['name'] == name:
            print 'the name is already in list'
            return
    new_subscribe = {'name': name, 'address': address,
                     'lastEpisode': lastEpisode, 'sourceName': sourceName}
    subscribe_list['list'].append(new_subscribe)
    subscribe_list['total'] += 1
    writeFile(json.dumps(subscribe_list))


def deleateSubscribeList(name):
    if not judgeSubscribeList():
        return
    index = 0
    content=readFile()
    subscribe=json.loads(content)
    subscribe_list=subscribe['list']
    for i in range(len(subscribe_list)):
        if name==subscribe_list[i]['name']:
            index = i
            break
    if index !=0:
        del subscribe_list[index]
        subscribe['total'] -= 1
        writeFile(json.dumps(subscribe))
    else:
        print 'the name is not existed'


def getUrl():
    url = []
    content = readFile()
    print type(content)
    subscribe_list = json.loads(content)
    list = subscribe_list['list']
    for i in list:
        url.append(i['address'])
    print type(url)
    return url


def updateLastEpisode(episodes):
    content = readFile()
    subscribe_list = json.loads(content)
    if subscribe_list:
        print 'the list is empty'
        return
    m = 0
    for i in subscribe_list['list']:
        i['lastEpisode'] = episodes[m]
        m += 1
    writeFile(json.dumps(subscribe_list))


# updateSubscribeList('abc','www.baidu.com',5,'Monday')
# deleateSubscribeList('abc')
#deleateSubscribeList(u'宝石之国')