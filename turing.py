# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2016/10/31'
#    __Desc__ = 图灵机器人测试

import requests
import urllib, urllib2
import json
import jieba
import pyttsx
from random import randint


# 一次性初始化语音引擎，减少资源的打开关闭开销
engine = pyttsx.init()


# 对语句进行分词，分词列表中将包含查询所需的关键字,这里暂且用不到了（接口已经完成了此项任务）
def parseText(text):
    words = []
    words = jieba.cut(text, cut_all=True)
    return list(set(words))


# 根据post方式获取到返回信息
def getResult(url, payload):
    res = requests.post(url=url, data=payload)
    return res

def getData(url, payload):
    payload = urllib.urlencode(payload)
    req = urllib2.Request(url=url, data=payload)
    return urllib2.urlopen(req).read()

# 初始化语音引擎，让电脑读出来
def say(text):
    rate = engine.getProperty('rate')
    # 控制一下语速
    engine.setProperty('rate', rate - 64 + randint(10, 36))
    engine.say(text)
    engine.runAndWait()


# 根据返回的code来判断属于哪一类的json数据串，方便接下来的拆解，共有
# 10 0000 文本类
# 20 0000 链接类
# 30 2000 新闻类
# 30 8000 菜谱类
# 31 3000 儿歌类（仅针对于儿童版）
# 31 4000 诗词类（仅针对于儿童版）
def switch(result):
    code = result['code']

    if code == 100000:
        text = result['text']
        print text
        say(text)

    elif code == 200000:
        text = result['text']
        url = result['url']
        print text, url
        say(text + '.    不妨，点击后面的链接查看详情吧')

    elif code == 302000:
        text = result['text']

        newslist = result['list']
        # 循环读取每一个条目的新闻内容
        for item in range(len(newslist)):
            article = newslist[item]['article']
            source = newslist[item]['source']
            detailurl = newslist[item]['detailurl']

            print article, source, detailurl

    elif code == 308000:
        text = result['text']
        menu = result['list']

        # 循环的打出每一条菜谱的详细信息
        for item in menu:
            name = item['name']
            icon = item['icon']
            info = item['info']
            detailurl = item['detailurl']

            print name, icon, info, detailurl

    else:
        print '我竟无言以对，╭(╯^╰)╮'
        say('我表示不知道说什么好了')


# 根据关键字的不同，组装出不同的post数据，以便于获取不同的结果集
def main(url='http://www.tuling123.com/openapi/api', text='你好'):
    payload = {
        'key': '318089813107c57c883dd1ce68c1bf70',
        'info': text,
        # userid 官网上说是针对每一个用户实现的不同的编号即可，这里随意指定不重复即可
        'userid': '1357924680'
    }
    # 将返回的数据以json的方式打开，并读取Reponse的内容部分
    # result = json.loads(getResult(url, payload).text)
    result = json.loads(getData(url, payload))
    # 根据code的不同，跳转到不同的分支，实现条件语句
    switch(result)


if __name__ == '__main__':
    print '嗨，我是专门为你打造的一个聊天机器人，随便和我聊些什么吧，我可以陪您聊天，给您讲笑话，查新闻，查航班，查车票，还能为您找菜谱呢(*^__^*) 嘻嘻……\n\n\n'.encode('gbk')
    username = raw_input('输入姓名后即可开始聊天，按Ctrl+C退出: '.encode('gbk'))
    question = raw_input('%s: '.encode('gbk') % username)
    while True:
        question = question.decode('gbk')
        main(text=question)
        print '---------------------------------------------------'
        question = raw_input('%s: '.encode('gbk') % username)
    print '( ^_^ )/~~拜拜'.encode('utf-8')
