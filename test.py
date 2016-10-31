# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2016/10/31'
#    __Desc__ = 


from turing import *

if __name__ == '__main__':
    url = 'http://www.tuling123.com/openapi/api'
    text = '讲个笑话吧'
    main(url, text)
    # payload = {
    #     'key': '318089813107c57c883dd1ce68c1bf70',
    #     'info': text,
    #     # userid 官网上说是针对每一个用户实现的不同的编号即可，这里随意指定不重复即可
    #     'userid': '1357924680'
    # }
    # print getData(url, payload)