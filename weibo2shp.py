# -*- coding: utf-8 -*-
import os
import re
import time
from decimal import Decimal

import shapefile as shp

import python_mysql as mydb


try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

#程序配置信息
fileFolder = u'D:\data\sinaweibodata'
suffix = u'.shp'
tableName = 'sinaweibo'

mysql_host = "localhost"
mysql_database = "weibo"
mysql_user = "root"
mysql_password = "ronald"

if '__main__' == __name__:
    #检验目标文件夹是否存在，不存在则创建
    if os.path.exists(fileFolder):
        pass
    else:
        os.makedirs(fileFolder)

    #连接数据库，找出表
    mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
    fileName = os.path.join(fileFolder, tableName) + suffix

    #检测文件是否存在
    if os.path.exists(fileName):
        os.remove(fileName)

    #使用分页的形式查询处理
    pcount = 1000
    #计算页数
    sql = 'select count(*) as count from %s' % tableName
    ctable = mysqlconn.query(sql)
    tcount = int(ctable[0]['count'])
    pages = tcount / pcount

    #创建shp文件结构
    w = shp.Writer(shp.POINT)
    w.field('id', 'C', '20')
    w.field('uid', 'C', '20')
    w.field('created_at', 'C', '30')
    w.field('reposts_count', 'C', '6')
    w.field('comments_count', 'C', '6')
    w.field('attitudes_count', 'C', '6')

    #lng和lat字段可能出现脏数据，需要模式识别，字段只能是类似于xxx.xxxxx的形式，不能出现其他非数字字符
    pattern = re.compile(r'\d+\.\d+$')

    for i in range(pages + 1):
        offset = i * pcount
        sql = 'select id, created_at, uid, lng, lat, reposts_count, comments_count, attitudes_count' \
              ' from %s limit %s,%s' % (tableName, str(offset), str(pcount))
        ttable = mysqlconn.query(sql)
        for row in ttable:
            rid = row['id']
            created_at = row['created_at']
            uid = row['uid']
            tlng = row['lng']
            tlat = row['lat']
            reposts_count = row['reposts_count']
            comments_count = row['comments_count']
            attitudes_count = row['attitudes_count']
            match_lng = pattern.match(tlng)
            if match_lng:
                match_lat = pattern.match(tlat)
                if match_lat:
                    lng = Decimal(match_lng.group(0))
                    lat = Decimal(match_lat.group(0))
                    w.point(lng, lat)
                    w.record(rid, uid, created_at, reposts_count, comments_count, attitudes_count)
            else:
                continue
            curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print '------%s / %s------%s' % (i, pages, curtime)
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print 'all record dealed, creating shp file...%s' % curtime
    shape = StringIO()
    shx = StringIO()
    dbf = StringIO()
    w.saveDbf(os.path.join(fileFolder, tableName))
    w.saveShp(os.path.join(fileFolder, tableName))
    w.saveShx(os.path.join(fileFolder, tableName))
    curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print '%s had created----%s ' % (fileName, curtime)




