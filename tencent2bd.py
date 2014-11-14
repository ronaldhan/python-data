# -*- coding: utf-8 -*-
import python_mysql as mydb
import urllib2
import urllib
import json
from decimal import Decimal

BaiDu_API_GeoConv = 'http://api.map.baidu.com/geoconv/v1/?'
BaiDu_API_AK = 'UjDN5L4WOmeoTAMIZG73MU1F'
BaiDu2Origin = 'http://api.zdoz.net/bd2wgs.aspx?'

mysql_host = "localhost"
mysql_database = "ftpoi"
mysql_user = "root"
mysql_password = "ronald"

if '__main__' == __name__:
    # 连接数据库，找出目标数据库中所有的表
    mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
    sql = "show tables"
    tableNames = mysqlconn.query(sql)
    for item in tableNames:
        tableName = item['Tables_in_ftpoi']
        sql = u'select id,lng,lat from %s' % tableName
        table = mysqlconn.query(sql)
        for row in table:
            rid = row['id']
            lng = row['lng'].strip()
            lat = row['lat'].strip()
            bdurl = BaiDu_API_GeoConv + 'coords=' + lng + ',' + lat + '&from=3&to=5&ak=' + BaiDu_API_AK
            response = urllib2.urlopen(bdurl).read()
            decodejson = json.loads(response)
            if decodejson['status'] != 0:
                continue
            else:
                bdlng = decodejson['result'][0]['x']
                bdlat = decodejson['result'][0]['y']
            ourl = BaiDu2Origin + 'lng=' + str(bdlng) + '&lat=' + str(bdlat)
            data = urllib2.urlopen(ourl).read()
            result = json.loads(data)
            if len(result) > 0:
                olng = result['Lng']
                olat = result['Lat']
            else:
                continue
            sql = "update %s set lng=%s,lat=%s where id=%s" % (tableName, str(olng), str(olat), rid)
            mysqlconn.execute(sql)
            mysqlconn.commit()
            print 'baidu:(%s,%s)---->origin:(%s,%s)' % (str(bdlng), str(bdlat), str(olng), str(olat))
        print '-----%s had finished------' % tableName
    print 'all tables had finished'
