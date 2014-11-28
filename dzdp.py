# -*- coding:utf-8 -*-
import requests
import python_mysql as mydb
from pyquery import PyQuery as pq
from decimal import Decimal
import time
import json
from dzdpconfig import *


class MyException(Exception):
    def __init__(self):
        Exception.__init__(self)
        print 'web request exception'


def process(item):
    ##处理一个条目，返回所有解析信息
    #部分信息在概略页获取，部分在详细页获取
    item = pq(item)
    try:
        shopname = item('.tit h4').text()
    except AttributeError:
        pass
    remark = item('.comment')
    try:
        grade = pq(remark)('span').attr('title')
    except AttributeError:
        grade = '-1'
    try:
        reviewnum = pq(remark)('.review-num b')
        if reviewnum:
            comment = reviewnum.text()
        else:
            reviewnum = pq(remark)('a')[0]
            reviewnum = pq(reviewnum)
            comment = reviewnum.text()
        #comment会出现没有点评的现象，需要进行字符串处理
        if comment == u'我要点评':
            comment = u'0'
    except AttributeError:
        comment = '-1'
    try:
        meanprice = pq(remark)('.mean-price b')
        if meanprice:
            avg = meanprice.text()
        else:
            meanprice = pq(remark)('.mean-price')
            avg = pq(meanprice).text()
        #可能没有价格信息
        if avg == u'-':
            avg = u'0'
    except AttributeError:
        avg = '-1'
    try:
        tagaddr = item('.tag-addr')
        tags = pq(tagaddr)('.tag').text()
        address = '海淀区' + pq(tagaddr)('.addr').text()
    except AttributeError:
        tags = '-1'
        address = '-1'
    #详细页获取信息
    hrefitem = item('.tit a')[0]
    href = pq(hrefitem).attr('href')
    itemurl = webroot + href
    itempage = requests.get(itemurl).text
    itemhtml = pq(itempage)
    try:
        phoneinfo = itemhtml('span').filter(lambda i: pq(this).attr('itemprop') == 'tel')
        if len(phoneinfo) == 0:
            phone = ''
            pass
        else:
            phone = pq(phoneinfo).text()
    except AttributeError:
        phone = '-1'
    try:
        yytime = ''
        other1 = itemhtml('.other p')
        for p in other1:
            p = pq(p)
            infoname = p('.info-name').text()
            if u'营业' in infoname:
                yytime = p('.item').text()
    except AttributeError:
        yytime = '-1'
    try:
        utags = ''
        for q in other1:
            q = pq(q)
            infoname = q('.info-name').text()
            if u'分类' in infoname:
                utags = q('.item').text().replace(' (', '(')
    except AttributeError:
        utags = '-1'
    print 'item %s dealed' % shopname
    return (shopname,grade,comment,avg,tags,address,phone,yytime,utags)


def getstate():
    #读取state文件，返回状态信息
    with open(sFile, 'r') as statefile:
        content = statefile.read()
        cjson = json.loads(content)
        sgroup = cjson["i"]
        spage = cjson["j"]
        return (sgroup,spage)


def setstate(sgroup=0, spage=1):
    #设置state文件，保存状态信息
    content = open(sFile, 'r').read()
    cjson = json.loads(content)
    with open(sFile, 'w') as statefile:
        cjson["i"] = sgroup
        cjson["j"] = spage
        sjson = json.dumps(cjson)
        statefile.write(sjson)


def getpage(url, count=5, interval=10):
    #尝试5次，失败后自动延长时间
    fpage = ''
    try:
        fpage = requests.get(url).text
        return fpage
    except Exception,ex:
        if count:
            stime = interval*(6 - count)
            print '将等待%s秒，第%s次重试……' % (str(stime), str(6 - count))
            time.sleep(stime)
            count -= 1
            value = getpage(url, count)
            return value
        else:
            return 'bad'


if __name__ == '__main__':
    mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
    urlFile = open(cFile, 'r')
    lines = urlFile.readlines()
    group = len(lines)/3
    sgroup, spage = getstate()
    try:
        for i in range(sgroup, group):
            #需要将行末的换行符去掉，最后一行单独处理
            if i < group - 1:
                kword = lines[3*i][:-1]
                firstUrl = lines[3*i + 1][:-1]
                nextUrl = lines[3*i + 2][:-1]
            else:
                kword = lines[3*i][:-1]
                firstUrl = lines[3*i + 1][:-1]
                nextUrl = lines[3*i + 2]
            print '第%s类-----%s开始' % (str(i), kword)
            fpage = getpage(firstUrl)
            if len(fpage) < 5000:
                raise MyException()
            html = pq(fpage)
            #获取总计有多少页
            tpage = html('.page a')[-2]
            totalnum = pq(tpage).text()
            total = Decimal(totalnum)
            for j in range(spage, total + 1):
                #nUrl = (j == 1) and firstUrl or nextUrl.replace('(*)', str(j))
                if j == 1:
                    nUrl = firstUrl
                else:
                    tUrl = nextUrl
                    nUrl = tUrl.replace('(*)', str(j))
                page = getpage(nUrl)
                if len(page) < 5000:
                    #警告页内容
                    raise MyException()
                nhtml = pq(page)
                nitems = nhtml('.shop-list ul li')
                for nitem in nitems:
                    shopname, grade, comment, avg, tags, address, phone, yytime, utags = process(nitem)
                    mysqlconn.insert(mysql_tablename,
                                     name=shopname,
                                     grade=grade,
                                     comment=comment,
                                     avg=avg,
                                     tags=tags,
                                     address=address,
                                     phone=phone,
                                     yytime=yytime,
                                     utags=utags,
                                     kword=kword)
                    time.sleep(7)
                mysqlconn.commit()
                print '%s--page %s--finished' % (kword, str(j))
            print '<---------------->'
            spage = 1
        print 'all finished'
    except Exception, ex:
        print ex.message
        #判断j变量是否初始化，没有初始化赋值1
        j = ('j' in locals().keys()) and j or 1
        setstate(i, j)
    finally:
        mysqlconn.close()
