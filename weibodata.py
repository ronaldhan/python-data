# -*- coding:utf-8 -*-
import time

import pymongo
import MySQLdb as mydb

from weibodataconfig import *


if __name__ == '__main__':
    mongo_connection = pymongo.Connection(mongo_host, mongo_port)
    mysql_connection = mydb.Connection(host=mysql_host, db=mysql_database, port=mysql_port,
                                       user=mysql_user, passwd=mysql_password)
    mysql_cursor = mysql_connection.cursor()
    mongo_db = mongo_connection['test']
    mongo_collections = mongo_db.collection_names()
    #list的remove方法没有返回值
    mongo_collections.remove('system.indexes')
    for collection in mongo_collections:
        user_collction = mongo_db[collection]
        total = user_collction.find().count()
        count = 0
        for post2json in user_collction.find():
            # post2json = json.loads(post)
            # find返回的就是json字符串，不需要在进行处理
            if 'id' in post2json.keys():
                pid = post2json['id']
            else:
                pid = ''
            # 两种判断键是否存在的方法
            if post2json.has_key('created_at'):
                created_at = post2json['created_at']
            else:
                created_at = ''
            if 'text' in post2json.keys():
                text = post2json['text']
            else:
                text = ''
            if 'user' in post2json.keys():
                userjson = post2json['user']
                if 'id' in userjson.keys():
                    uid = userjson['id']
                if 'province' in userjson.keys():
                    province = userjson['province']
                if 'city' in userjson.keys():
                    city = userjson['city']
                if 'location' in userjson.keys():
                    location = userjson['location']
                if 'gender' in userjson.keys():
                    gender = userjson['gender']
                if 'followers_count' in userjson.keys():
                    followers_count = userjson['followers_count']
                if 'friends_count' in userjson.keys():
                    friends_count = userjson['friends_count']
                if 'statuses_count' in userjson.keys():
                    statuses_count = userjson['statuses_count']
                if 'favourites_count' in userjson.keys():
                    favourites_count = userjson['favourites_count']
                if 'created_at' in userjson.keys():
                    user_created_at = userjson['created_at']
                if 'bi_followers_count' in userjson.keys():
                    bi_followers_count = userjson['bi_followers_count']
            else:
                uid = province = city = location = gender = followers_count = friends_count \
                    = statuses_count = favourites_count = user_created_at = bi_followers_count = ''
            if 'geo' in post2json.keys():
                if 'coordinates' in post2json['geo'].keys():
                    geo_lng = post2json['geo']['coordinates'][0]
                    geo_lat = post2json['geo']['coordinates'][1]
            else:
                geo_lng = ''
                geo_lat = ''
            if 'retweeted_status' in post2json.keys():
                retweeted_status = post2json['retweeted_status']
            else:
                retweeted_status = ''
            if 'reposts_count' in post2json.keys():
                reposts_count = post2json['reposts_count']
            else:
                reposts_count = ''
            if 'comments_count' in post2json.keys():
                comments_count = post2json['comments_count']
            else:
                comments_count = ''
            if 'attitudes_count' in post2json.keys():
                attitudes_count = post2json['attitudes_count']
            else:
                attitudes_count = ''
            # print text
            sql = 'insert into %s ' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                  '' % (mysql_weibodata, pid, created_at,
                        text, uid, geo_lng, geo_lat, retweeted_status,
                        reposts_count, comments_count, attitudes_count)
            mysql_cursor.execute(sql)
            # mysql_connection.insert(mysql_weibodata,
            #                         id=pid,
            #                         created_at=created_at,
            #                         text=text,
            #                         uid=uid,
            #                         geo_lng=geo_lng,
            #                         geo_lat=geo_lat,
            #                         retweeted_status=retweeted_status,
            #                         reposts_count=reposts_count,
            #                         comments_count=comments_count,
            #                         attitudes_count=attitudes_count)
            # mysql_connection.insert(mysql_weibouser,
            #                         uid=uid,
            #                         province=province,
            #                         city=city,
            #                         location=location,
            #                         gender=gender,
            #                         followers_count=followers_count,
            #                         friends_count=friends_count,
            #                         statuses_count=statuses_count,
            #                         favourites_count=favourites_count,
            #                         created_at=user_created_at,
            #                         bi_followers_count=bi_followers_count)
            sql = 'insert into %s ' \
                  'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)' \
                  '' % (mysql_weibouser, uid, province,
                        city, location, gender, followers_count, friends_count,
                        statuses_count, favourites_count, user_created_at, bi_followers_count)
            mysql_cursor.execute(sql)
            mysql_connection.commit()
            count += 1
            curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if count % 100 == 0:
                print '%s----->%s/%s<------' % (curtime, str(count), str(total))
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print '%s----->%s dealed' % (curtime, collection)
    print 'all record finished'