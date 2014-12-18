# -*- coding: utf-8 -*-
import python_mysql as mydb
import urllib2
import json
import time

BaiDu_API_AK = 'UjDN5L4WOmeoTAMIZG73MU1F'
BaiDu2Origin = 'http://api.zdoz.net/bd2wgs.aspx?'

mysql_host = "localhost"
mysql_database = "bjdata"
mysql_user = "root"
mysql_password = "ronald"
tablename = 'bdditu1'

if '__main__' == __name__:
    mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
    sql = u'select id,lng,lat from %s where id > 14420' % tablename
    table = mysqlconn.query(sql)
    for row in table:
        rid = row['id']
        lng = row['lng'].strip()
        lat = row['lat'].strip()
        ourl = BaiDu2Origin + 'lng=' + str(lng) + '&lat=' + str(lat)
        data = urllib2.urlopen(ourl).read()
        result = json.loads(data)
        if len(result) > 0:
            olng = result['Lng']
            olat = result['Lat']
        else:
            continue
        sql = "update %s set lng=%s,lat=%s where id=%s" % (tablename, str(olng), str(olat), rid)
        mysqlconn.execute(sql)
        mysqlconn.commit()
        print 'record %s: baidu:(%s,%s)---->origin:(%s,%s)' % (rid, str(lng), str(lat), str(olng), str(olat))
        time.sleep(0.1)
    print 'table %s finished' % tablename

