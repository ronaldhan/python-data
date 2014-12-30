# -*- coding:utf-8 -*-
import requests
import python_mysql as mydb
from ftconfig import *
import time
import re


if __name__ == '__main__':
    mysqlconn = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
    #使用分页的形式查询处理
    pcount = 100
    #存储checkin数量的字段
    check_column = 'checksum'
    pattern = re.compile(r'[+-]?\D+$')
    sql = 'select count(*) as count from %s' % mysql_tablename
    ctable = mysqlconn.query(sql)
    tcount = int(ctable[0]['count'])
    pages = tcount / pcount
    for i in range(pages + 1):
        offset = i * pcount
        sql = 'select id, uid from %s limit %s,%s' % (mysql_tablename, str(offset), str(pcount))
        ttable = mysqlconn.query(sql)
        for row in ttable:
            rid = row['id']
            dparams['uid'] = row['uid']
            #如果网络连接有问题，重试三次
            for k in range(3):
                try:
                    r = requests.get(BD_API_DETAIL, params=dparams)
                    break
                except:
                    print 'connection err retrying'
                    time.sleep(5)
            result = r.json()
            if result['status'] == 0:
                detailinfo = result['result']['detail_info']
                #判断是否有checkin_num属性
                if 'checkin_num' in detailinfo.keys():
                    checkin_num = detailinfo['checkin_num']
                    #checkin可能不是纯数字，需要验证
                    match = pattern.match(checkin_num)
                    if match is None:
                        sql = 'update %s set %s=%s where id=%s' % (mysql_tablename, check_column, checkin_num, rid)
                        mysqlconn.execute(sql)
                    else:
                        print '%s return bad result' % rid
                        continue
                else:
                    continue
            else:
                print '%s return bad result' % rid
        #一页结果处理结束后再提交
        mysqlconn.commit()
        print 'the %s / %s finished' % (i, pages)
        time.sleep(60)
    print '--all--'