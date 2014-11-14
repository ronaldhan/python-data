# -*- coding: utf-8 -*-

import sqlite3 as lite
import MySQLdb
import python_mysql as mydb

try:
        dbPath="C:/Program Files (x86)/火车采集器V8/Data"
        fileName="/5/SpiderResult.db3"
        tableName='yhxxl'
        conn=lite.connect(dbPath+fileName)
        conn.row_factory=lite.Row
        cur=conn.cursor()
        #cur.execute('select * from Content')        
        #col_name_list=[tuple[0] for tuple in cur.description]
        #print col_name_list
##        for item in col_name_list:
##                print item,
##        print
        
##        res=cur.fetchone()
##        for item in res:
##                print item,
##        print
        cur.execute('select * from sqlite_master where type="table" and name="Content"')
        row=cur.fetchone()
        #the 4th field is the create sql
        #print row[4]
        sql=row[4].replace('[','`').replace(']','`').replace('autoincrement','auto_increment').replace('Content',tableName)
        sql=sql.replace('已采','yc').replace('已发','yf').replace('名称','name').replace('地址','address').replace('标签','tags').replace('星级','grade').replace('点评数','comment')
        #print sql
        #connect to mysql
        #check if the table exists
        #if the table not exists result is []
        #mysqlconn=mydb.Connection(host="localhost",user="root",passwd="ronald",db="ftpoi",port=3306)        
        #mycur=mysqlconn.cursor()
        #exist=mycur.execute('show tables like %s','%'+tableName+'%')
        #print exist
##        if exist ==0:
##                mycur.execute(sql)
##        else:
##                pass
##        cur.execute('select * from Content')
##        rows=cur.fetchall()
##        for row in rows:
##                sqlstr="insert into " + tableName + " values(%s,%s,%s,%s,%s,%s,%s,%s)"
##                values=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
##                cur.execute(sqlstr,values)
        mysqlconn=mydb.Connection(host="localhost",database="ftpoi",user="root",password="ronald")
        exist=mysqlconn.query('show tables like %s','%'+tableName+'%')
        if exist==[]:
                #create new table
                mysqlconn.execute(sql)               
        else:
                pass
        mysqlconn2=MySQLdb.Connection(host="localhost",user="root",passwd="ronald",db="ftpoi",port=3306,charset="utf8")        
        mycur=mysqlconn2.cursor()
        #get all data in sqlite
        #insert into mysql
        cur.execute('select * from Content')
        rows=cur.fetchall()
        for row in rows:
##                #sqlstr="insert into " + tableName + " ('已采','已发','名称','地址','标签','星级','点评数','PageUrl') values (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])"
##                #mysqlconn.insert(tableName,"已采"=row[1],"已发"=row[2],"名称"=row[3],"地址"=row[4],"标签"=row[5],"星级"=row[6],"点评数"=row[7],"PageUrl"=row[8])
##                #mysqlconn.commit()
                sqlstr="insert into " + tableName + " ('已采','已发','名称','地址','标签','星级','点评数','PageUrl') values(%s,%s,%s,%s,%s,%s,%s,%s)"
                values=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
                mycur.execute(sqlstr,values)
                
##        for items in rows:
##                for item in items:
##                        print item,
##        print
        
        #print exist
        cur.close()
        conn.close()
        mycur.close()
        mysqlconn.close()
        mysqlconn2.close()
except Exception, e:
        raise
else:
        pass
finally:
        pass
