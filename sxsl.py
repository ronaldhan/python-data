# -*- coding:utf-8 -*-
import urllib2
from pyquery import PyQuery as pq
import urllib
import python_mysql as mydb
import datetime
import time

mysql_host = "localhost"
mysql_database = "test"
mysql_user = "root"
mysql_password = "ronald"
tableName = 'sxsl1'

mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
rURL = 'http://www.ctg.com.cn/inc/sqsk.php'
##ST = datetime.date(2000, 01, 01)
ST = datetime.date(2012, 11, 01)
##ET = datetime.date(1999, 9, 30)
ET = datetime.date(2012, 12, 31)
timedelta = ET - ST
daycount = timedelta.days + 1
for i in range(daycount):
    date = ST + datetime.timedelta(days=i)
    sdate = date.isoformat()
    values = {'NeedCompleteTime2': sdate}
    pdata = urllib.urlencode(values)
    req = urllib2.Request(rURL, pdata)
    page = urllib2.urlopen(req)
    fh = page.read()
    data = pq(fh)
    pf = open(r'D:\data\sxsl\pf' + sdate + '.txt', 'wb')
    pf.write(fh)
    t1 = data('body > table:eq(4)')
    #上方的四个表
    t3 = pq(t1).find("[width='50%']")
    for table in t3:
        #获取表头名称
        row1 = pq(table).find('div').text()
        # print row1
        # print '---------------'
        rowN = pq(table).find('tr')
        #对第四个表的解析有问题，需添加此判断
        if len(rowN) >= 5:
            rowN = rowN[1:]
        elif len(rowN) < 4:
            continue
        else:
            pass
        for row in rowN:
            detail = pq(row).find('td').text()
            tmp = detail.split(' ')
            value = tmp[0]
            xtime = tmp[1]
            # print value, time
            mysqlconn.insert(tableName, name=row1, date=sdate, time=xtime, value=value)
            mysqlconn.commit()
        # print '==============='
    #下方的12个表
    t2 = data('body > table:eq(6)')
    t4 = pq(t2).find("[width='14%']")
    for table1 in t4:
        row1 = pq(table1).find('div').text()
        # print row1
        # print '---------------'
        rowM = pq(table1).find('tr')
        if len(rowM) >= 5:
            rowM = rowM[1:]
        elif len(rowM) < 4:
            continue
        else:
            pass
        for row in rowM:
            detail = pq(row).find('td').text()
            tmp = detail.split(' ')
            value = tmp[0]
            xtime = tmp[1]
            # print value, time
            mysqlconn.insert(tableName, name=row1, date=sdate, time=xtime, value=value)
            mysqlconn.commit()
        # print '==============='
    print '------%s finished------' % sdate
    time.sleep(1)
print '%s----->%s finished' % (ST.isoformat(), ET.isoformat())
