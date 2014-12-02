# -*- coding: utf-8 -*-
import python_mysql as mydb
import os
import shapefile as shp
from decimal import Decimal
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

#程序配置信息
fileFolder = u'D:\data\shp'
suffix = u'.shp'
tableName = 'bdditu'

mysql_host = "localhost"
mysql_database = "bjdata"
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
    #print fileName
    #检测文件是否存在
    if os.path.exists(fileName):
        os.remove(fileName)
    sql = u'select * from %s' % tableName
    table = mysqlconn.query(sql)

    w = shp.Writer(shp.POINT)
    w.field('id', 'C', '8')
    w.field('name', 'C', '100')
    w.field('address', 'C', '100')
    w.field('catalog', 'C', '10')
    w.field('subcatalog', 'C', '20')
    for row in table:
        id = row['id']
        name = row['name'].strip().decode('utf-8').encode('cp936')
        address = row['address'].strip().decode('utf-8').encode('cp936')
        catalog = row['catalog']
        subcatalog = row['subcatalog'].decode('utf-8').encode('cp936')
        lng = Decimal(row['lng'].strip())
        lat = Decimal(row['lat'].strip())
        w.point(lng, lat)
        w.record(id, name, address, catalog, subcatalog)
        print '%s dealed' % id
    shape = StringIO()
    shx = StringIO()
    dbf = StringIO()
    #w.save(os.path.join(fileFolder, tableName), shape, shx, dbf)
    w.saveDbf(os.path.join(fileFolder, tableName))
    w.saveShp(os.path.join(fileFolder, tableName))
    w.saveShx(os.path.join(fileFolder, tableName))
    print '%s had created' % fileName




