# -*- coding:utf-8 -*-
import requests
import python_mysql as mydb
from ftconfig import *
import time


mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
#遍历catalog
for k, v in catalogs.iteritems():
    catalog = str(k)
    for word in v:
        kword = word + ' 丰台区'
        params['q'] = kword
        for key, religion in religions.iteritems():
            bounds = ','.join(religion)
            params['bounds'] = bounds
            params['page_num'] = 0
            r = requests.get(BD_API_PLACE, params=params)
            result = r.json()
            if result['status'] == 0:
                #正常返回结果,获取结果总数
                total = result['total']
                if total:
                    times = total/int(params['page_size'])
                    times += 1
                    #分页取回结果
                    for i in range(times):
                        params['page_num'] = str(i)
                        rr = requests.get(BD_API_PLACE, params=params)
                        fresult = rr.json()
                        if fresult['status'] == 0:
                            results = fresult['results']
                            for item in results:
                                #有些结果并没有address，需要判断
                                if 'address' in item.keys():
                                    mysqlconn.insert(mysql_tablename,
                                                     name=item['name'],
                                                     address=item['address'],
                                                     lng=str(item['location']['lng']),
                                                     lat=str(item['location']['lat']),
                                                     catalog=catalog,
                                                     subcatalog=word,
                                                     uid=item['uid'])
                                else:
                                    continue
                            mysqlconn.commit()
                            time.sleep(1)
                        else:
                            print 'XXXXX %s %s bound:%s page:%s  not finished XXXXX' % (catalog, word, str(key), str(i))
                        print '~~~~~ %s %s bound:%s page:%s finished ~~~~~' % (catalog, word, str(key), str(i))
                else:
                    print 'XXXXX %s %s bound:%s total:%s XXXXX' % (catalog, word, str(key), str(total))
                    continue
            else:
                print 'XXXXX %s %s bound:%s not finished XXXXX' % (catalog, word, str(key))
            print '~~~~~ %s %s bound:%s finished ~~~~~' % (catalog, word, str(key))
        print '~~~~~ %s %s finished ~~~~~' % (catalog, word)
    print '~~~~~ %s finished ~~~~~' % catalog
print '~~~~~ all finished ~~~~~'
mysqlconn.close()