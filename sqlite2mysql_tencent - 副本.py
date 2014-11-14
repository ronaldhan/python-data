# -*- coding: utf-8 -*-
import os
import sqlite3 as lite
import python_mysql as mydb
import urllib2
import json
import time
#import config

#把字符转换为utf8编码就没有问题了
dbPath = u'C:\\Program Files (x86)\\火车采集器V8\\Data'
fileName = "SpiderResult.db3"
keyWord = u'丰台'
ids={
    'g237':'bank',
    'g979':'company',
    'g6120':'dry_cleaner',
    'g181':'hospital',
    'g260':'school',
    'g196':'training',
    'g197':'traveling',
    'g26117':'maintenance',
    'g836':'property',
    'g26466':'bbuilding',
    '10':'food',
    '30':'entertainment',
    'n10':'hotel',
    '50':'figure',
    '20':'shopping',
    '45':'fitness'
}

mysql_host="localhost"
mysql_database="ftpoi"
mysql_user="root"
mysql_password="ronald"

city=u"北京市"
tencentAPI_geocoding=u"http://apis.map.qq.com/ws/place/v1/search"
tencent_api_ak=u"46IBZ-DGRRV-LRGPO-UTXFR-RWSBT-BFFJN"

if '__main__' == __name__:        
        dirs=os.listdir(dbPath)
        #去掉最后一个
        dirs=dirs[:-1]
        print dirs
        #循环处理所有文件夹中的数据
        for subdir in dirs:
                filepath=os.path.join(dbPath,subdir)                
                conn=lite.connect(os.path.join(filepath,fileName))
                conn.row_factory=lite.Row
                cur=conn.cursor()
                #选取第一条记录，从url中分析类别
                cur.execute('select min(id),pageurl from Content')
                row=cur.fetchone()
                #提取大类编码
                kind=row[1].split('_')[0][-2:]
                #80对应的是细分类别
                if kind =='80':
                        #细分类别第一页和其他页的url不同
                        #包含‘#’的为首页
                        tmp=row[1].split('/')[-1]
                        if '#' in tmp:
                                kind=tmp.split('#')[0]
                        else:
                                kind=tmp[:f.find('p')]
                tableName=ids[kind]
                cur.execute('select * from sqlite_master where type="table" and name="Content"')
                row=cur.fetchone()
                #the 4th field is the create sql
                #print row[4]
                sql=row[4].replace('[','`').replace(']','`').replace('autoincrement','auto_increment').replace('Content',tableName)
                tmpsql=sql.split(',')
                #删除已发和已采字段
                del tmpsql[1:3]
                #重新组装sql语句
                sql=','.join(tmpsql)
                sql=sql.replace('名称','name').replace('标签','tags').replace('星级','grade').replace('点评数','comment')
                # add new column to table
                sql = sql[:-2] + ",`lng` Text,`lat` Text )"
                mysqlconn=mydb.Connection(host=mysql_host,database=mysql_database,user=mysql_user,password=mysql_password)
                psql="show tables like '%s'" %tableName
                #print psql
                exist=mysqlconn.query(psql)
                #print exist
                if exist==[]:
                        #create new table
                        mysqlconn.execute(sql)               
                else:
                        #delete old table then create new table
                        esql="drop table %s" %tableName
                        mysqlconn.execute(esql)
                        mysqlconn.execute(sql)
                
                #get all data in sqlite
                #insert into mysql
                cur.execute('select * from Content')
                rows=cur.fetchall()
                
                lng=""
                lat=""
                for row in rows:
                        #判断name字段是否为空
                        if row[3] is None:
                                continue
                        else:
                                name=row[3].strip()
                                print name
                                requestURI=tencentAPI_geocoding + u"?key=" +tencent_api_ak+ u"&keyword="+name+ u"&boundary=region("+city+ u",0)"
                                #requestURI='http://apis.map.qq.com/ws/place/v1/search?key=46IBZ-DGRRV-LRGPO-UTXFR-RWSBT-BFFJN&keyword=COSTA%20COFFEE(%E5%A4%A7%E5%B3%A1%E8%B0%B7%E8%B4%AD%E7%89%A9%E4%B8%AD%E5%BF%83%E5%BA%97)&boundary=region(%E5%8C%97%E4%BA%AC%E5%B8%82,0)'
                                print "请求地址为%s" % requestURI
                                fd=urllib2.urlopen(requestURI)
                                response=fd.read()
                                decodejson=json.loads(response)
                                #结果中包含正常返回的数据
                                if len(decodejson['data'])>0:
                                        #如果有多个结果，需要进行筛选，选择地址包含‘丰台区’的第一个结果
                                        #data中的address中可能包含多个数据，是一个元组
                                        index=0
                                        iscontain=False
                                        #需要判断是否包含有结果
                                        for result in decodejson['data']:                                        
                                                addr=result['address']
                                                if addr.find(keyWord) != -1:
                                                        iscontain = True
                                                        break
                                                #item这种方式是取单个字符，而不是单词，所以iscontain的结果不对
                                                # for item in addr:
                                                #         if keyWord in item:
                                                #                 iscontain = True
                                                #                 break
                                                #判断是否已经有满足条件的结果
                                                if index >= 0:
                                                        break
                                                else:
                                                        index = index + 1
                                        print '是否有结果:%s，索引为:%s' %(iscontain,index)
                                        #有满足条件的记录则插入数据库中
                                        if iscontain is True:
                                                #第一个满足条件的结果中提取经纬度       
                                                lng=decodejson['data'][index]['location']['lng']
                                                lat=decodejson['data'][index]['location']['lat']
                                                mysqlconn.insert(tableName,name=row[3],tags=row[4],grade=row[5],comment=row[6],PageUrl=row[7],lng=lng,lat=lat)
                                                mysqlconn.commit()
                                                print "记录(%s,%s,%s,%s,%s,%s,%s,%s,%s)已写入数据库" % (row[1],row[2],row[3],row[4],row[5],row[6],row[7],lng,lat)
                                                
                                        else:
                                                pass
                                        time.sleep(0.5)
                                else:
                                        pass
##                                mysqlconn.insert(tableName,name=row[3],tags=row[4],grade=row[5],comment=row[6],PageUrl=row[7],lng=lng,lat=lat)
##                                mysqlconn.commit()
##                                print "记录(%s,%s,%s,%s,%s,%s,%s,%s,%s)已写入数据库" % (row[1],row[2],row[3],row[4],row[5],row[6],row[7],lng,lat)
##                                time.sleep(0.5)
                cur.close()
                conn.close()
                mysqlconn.close()
                print tableName + " tranfor from sqlite 2 mysql finished"        
