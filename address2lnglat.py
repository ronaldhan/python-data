# -*- coding: utf-8 -*-
import urllib2
import json
import python_mysql as mydb

try:
	address="丰台区蒲方路芳古园一区29号楼通润商务会馆1楼"
	#address="二七广场"
	city="北京市"
	BaiDuAPI_Geocoding="http://api.map.baidu.com/geocoder/v2/"
	api_ak="UjDN5L4WOmeoTAMIZG73MU1F"
	requestURI=BaiDuAPI_Geocoding + "?ak=" +api_ak+"&address="+address+"&output=json"+"&city="+city
	fd=urllib2.urlopen(requestURI)
	response=fd.read()
	print response
	decodejson=json.loads(response)
	#如果查询没有结果，则result为[]
	if 'results' not in decodejson.keys():
		print "lng:%s;lat:%s" % (decodejson['result']['location']['lng'],decodejson['result']['location']['lat'])
	else:
		print "未找到查询的结果"
	fd.close()
	# print "recive",fd.geturl()
	# info=fd.info()
	# for key,value in info.items():
	# 	print "%s = %s" % (key,value)
except Exception, e:
	raise
else:
	pass
finally:
	pass