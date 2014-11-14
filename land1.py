# -*- coding:utf-8 -*-
import urllib2
from pyquery import PyQuery as pq
import urllib
import python_mysql as mydb
import time

root = 'http://www.bjgtj.gov.cn'
url = 'http://www.bjgtj.gov.cn/tabid/3259/Default.aspx'
next = r'ess$ctr5077$LandSoldList$WebUserPager1$lbtnNextPage'
first = r'ess$ctr5077$LandSoldList$WebUserPager1$lbtnFirstPage'
last = r'ess$ctr5077$LandSoldList$WebUserPager1$lbtnLastPage'

mysql_host = "localhost"
mysql_database = "ftpoi"
mysql_user = "root"
mysql_password = "ronald"
tableName = 'bj_land'

mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)

# 读取第一页的内容，获取下一页的请求信息和总页数
page = urllib2.urlopen(url)
fh = page.read()
pf = open(r'C:\Users\sony\Desktop\test\webfile\pf1.txt', 'wb')
pf.write(fh)
data = pq(fh)
viewstate = data("input[name='__VIEWSTATE']").attr('value')
totalNum = int(data("#ess_ctr5077_LandSoldList_WebUserPager1_lblPageInfo").text().split(',')[1].split('/')[1])
#20条数据的四列值
table = data('.datagrid-main tr:gt(0)')
#获取每个条目的网络路径
linksObj = table('a')

for item in linksObj:
    #values样例
    #['ess_ctr5077_LandSoldList_grdList_ctl05_hlnkView',
    #'/tabid/3259/ctl/LandSoldView/mid/5077/id/100021805/Default.aspx']
    link = item.values()[1]
    #拼接详细信息的url
    detailURL = root + link
    # detailURL = 'http://www.bjgtj.gov.cn/tabid/3259/ctl/LandSoldView/mid/5077/id/100021807/Default.aspx'
    detail = urllib2.urlopen(detailURL)
    fh = pq(detail.read())
    #样例数据
    #受让方名称：土地位置：区县：宗地面积：规划建筑面积：规划用途：土地成交价：宗地四至：签约时间：
    #合同约定开工时间：合同约定竣工时间：容积率(地上)：发布时间
    rows = fh("#ess_ctr5077_ModuleContent tr:lt(13)")
    colCount = 0
    colName = {}
    for row in rows:
        #样例数据
        #受让方名称： 北京市顺义大龙城乡建设开发总公司
        #中间的中文分号需要注意
        txt = pq(row).find('span').text()
        #此步骤将文本转码，所以下面需要对其进行复原
        txt = txt.decode('utf-8').encode('cp936')
        txt = txt.split('：'.decode('utf-8').encode('cp936'))
        #此步骤非常重要，不进行转码会导致报1406错误，不能写入数据，编码复原为utf8
        rtxt = txt[1].decode('cp936').encode('utf-8')
        # print col,rtxt
        colName[colCount] = rtxt
        colCount = colCount + 1
    mysqlconn.insert(tableName,
                     receiver=colName[0],
                     location=colName[1],
                     county=colName[2],
                     area=colName[3],
                     parea=colName[4],
                     usage=colName[5],
                     price=colName[6],
                     zdsz=colName[7],
                     dealdate=colName[8],
                     htkgdate=colName[9],
                     htjgdate=colName[10],
                     volume=float(colName[11]),
                     publicdate=colName[12])
    mysqlconn.commit()
    print '--------'
    for k,v in colName.items():
        print k,v
print '<------第一页处理完毕------>'
time.sleep(1)
#处理剩余的页面内容
for i in range(totalNum)[:-1]:
    #定义需要post的数据
    values = {
        '__EVENTTARGET': 'ess$ctr5077$LandSoldList$WebUserPager1$lbtnNextPage',
        'ess$ctr5077$LandSoldList$ddlYear': 0,
        'ess$ctr5077$LandSoldList$ddlMonth': 0,
        '__VIEWSTATE': viewstate
    }
    pdata = urllib.urlencode(values)
    req = urllib2.Request(url, pdata)
    pageN = urllib2.urlopen(req)
    fhN = pageN.read()    
    dataN = pq(fhN)
    fileNum = str(i+2)
    pfN = open(r'C:\Users\sony\Desktop\test\webfile\pf' + fileNum + '.txt', 'wb')
    pfN.write(fhN)
    viewstate = dataN("input[name='__VIEWSTATE']").attr('value')
    table = dataN('.datagrid-main tr:gt(0)')
    #获取每个条目的网络路径
    linksObj = table('a')
    for item in linksObj:
        #values样例
        #['ess_ctr5077_LandSoldList_grdList_ctl05_hlnkView',
        #'/tabid/3259/ctl/LandSoldView/mid/5077/id/100021805/Default.aspx']
        link = item.values()[1]
        #拼接详细信息的url
        detailURL = root + link
        # detailURL = 'http://www.bjgtj.gov.cn/tabid/3259/ctl/LandSoldView/mid/5077/id/100021807/Default.aspx'
        detail = urllib2.urlopen(detailURL)
        fh = pq(detail.read())
        #样例数据
        #受让方名称：土地位置：区县：宗地面积：规划建筑面积：规划用途：土地成交价：宗地四至：签约时间：
        #合同约定开工时间：合同约定竣工时间：容积率(地上)：发布时间
        rows = fh("#ess_ctr5077_ModuleContent tr:lt(13)")
        colCount = 0
        #此处使用字典前需要将其清空
        colName = {}
        for row in rows:
            #样例数据
            #受让方名称： 北京市顺义大龙城乡建设开发总公司
            #中间的中文分号需要注意
            txt = pq(row).find('span').text()
            #此步骤将文本转码，所以下面需要对其进行复原
            txt = txt.decode('utf-8').encode('cp936')
            txt = txt.split('：'.decode('utf-8').encode('cp936'))
            #此步骤非常重要，不进行转码会导致报1406错误，不能写入数据，编码复原为utf8
            #不太清楚为什么会有长度为3的情况，编码问题？先标记下，再处理数据库中记录吧
            if len(txt) > 2:
                rtxt = 'none'
            else:
                rtxt = txt[1].decode('cp936').encode('utf-8')
            # print col,rtxt
            colName[colCount] = rtxt            
            colCount = colCount + 1
        mysqlconn.insert(tableName,
                         receiver=colName[0],
                         location=colName[1],
                         county=colName[2],
                         area=colName[3],
                         parea=colName[4],
                         usage=colName[5],
                         price=colName[6],
                         zdsz=colName[7],
                         dealdate=colName[8],
                         htkgdate=colName[9],
                         htjgdate=colName[10],
                         volume=colName[11],
                         publicdate=colName[12])
        mysqlconn.commit()
        print '--------'
        for k,v in colName.items():
            print k,v
    print '<------第%s页处理完毕------>' %str(i+2)
    time.sleep(1)
print '<------总计%s页处理完毕------>' %str(totalNum)
