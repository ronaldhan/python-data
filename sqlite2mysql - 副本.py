import os

try:
        dbPath="C:\\Program Files (x86\\火车采集器V8\\Data"
        fileName="SpiderResult.db3"
        dirs=os.listdir(dbPath)
        for item in dirs:
                path=os.path.join(dbPath,item)
                print os.path.join(path,fileName)
        # tableName='bank'
        # conn=lite.connect(dbPath+fileName)
        # conn.row_factory=lite.Row
        # cur=conn.cursor()
        # cur.execute('select * from sqlite_master where type="table" and name="Content"')
        # row=cur.fetchone()
        # #the 4th field is the create sql
        # #print row[4]
        # sql=row[4].replace('[','`').replace(']','`').replace('autoincrement','auto_increment').replace('Content',tableName)
        # sql=sql.replace('已采','yc').replace('已发','yf').replace('名称','name').replace('地址','address').replace('标签','tags').replace('星级','grade').replace('点评数','comment')
        # # add new column to table
        # sql = sql[:-2] + ",`lng` Text,`lat` Text )"
        # mysqlconn=mydb.Connection(host="localhost",database="ftpoi",user="root",password="ronald")
        # exist=mysqlconn.query('show tables like %s','%'+tableName+'%')
        # if exist==[]:
                # #create new table
                # mysqlconn.execute(sql)               
        # else:
                # pass
        
        # #get all data in sqlite
        # #insert into mysql
        # cur.execute('select * from Content')
        # rows=cur.fetchall()

        # city="北京市"
        # BaiDuAPI_Geocoding="http://api.map.baidu.com/geocoder/v2/"
        # api_ak="UjDN5L4WOmeoTAMIZG73MU1F"
        # lng=""
        # lat=""
        # for row in rows:                
                # #mysqlconn.insert(tableName,"已采"=row[1],"已发"=row[2],"名称"=row[3],"地址"=row[4],"标签"=row[5],"星级"=row[6],"点评数"=row[7],"PageUrl"=row[8])
                # address=row[4].strip()                
                # requestURI=BaiDuAPI_Geocoding + "?ak=" +api_ak+"&address="+address+"&output=json"+"&city="+city
                # fd=urllib2.urlopen(requestURI)
                # response=fd.read()
                # decodejson=json.loads(response)
                # if 'results' not in decodejson.keys():
                        # lng=decodejson['result']['location']['lng']
                        # lat=decodejson['result']['location']['lat']
                # else:
                        # pass
                # mysqlconn.insert(tableName,yc=row[1],yf=row[2],name=row[3],address=row[4],tags=row[5],grade=row[6],comment=row[7],PageUrl=row[8],lng=lng,lat=lat)
                # mysqlconn.commit()
                # print "记录(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)已写入数据库" % (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],lng,lat)
        # cur.close()
        # conn.close()
        # mysqlconn.close()
        # print tableName + " tranfor from sqlite 2 mysql finished"
except Exception, e:
        raise
else:
        pass
finally:
        pass
