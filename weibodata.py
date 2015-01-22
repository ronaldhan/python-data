# -*- coding:utf-8 -*-
import json
import time

import pymongo
import python_mysql as mydb

from weibodataconfig import *


if __name__ == '__main__':
    mongo_connection = pymongo.Connection(mongo_host, mongo_port)
    mysql_connection = mydb.Connection(host=mysql_host, database=mysql_database,
                                       user=mysql_user, password=mysql_password)
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
            if hasattr(post2json, 'id'):
                pid = post2json['id']
            else:
                pid = ''
            if hasattr(post2json, 'created_at'):
                created_at = post2json['created_at']
            else:
                created_at = ''
            if hasattr(post2json, 'text'):
                text = post2json['text']
            else:
                text = ''
            if hasattr(post2json, 'user'):
                userjson = post2json['user']
                if hasattr(userjson, 'id'):
                    uid = userjson['id']
                if hasattr(userjson, 'province'):
                    province = userjson['province']
                if hasattr(userjson, 'city'):
                    city = userjson['city']
                if hasattr(userjson, 'location'):
                    location = userjson['location']
                if hasattr(userjson, 'gender'):
                    gender = userjson['gender']
                if hasattr(userjson, 'followers_count'):
                    followers_count = userjson['followers_count']
                if hasattr(userjson, 'friends_count'):
                    friends_count = userjson['friends_count']
                if hasattr(userjson, 'statuses_count'):
                    statuses_count = userjson['statuses_count']
                if hasattr(userjson, 'favourites_count'):
                    favourites_count = userjson['favourites_count']
                if hasattr(userjson, 'created_at'):
                    user_created_at = userjson['created_at']
                if hasattr(userjson, 'bi_followers_count'):
                    bi_followers_count = userjson['bi_followers_count']
            else:
                uid = province = city = location = gender = followers_count = friends_count \
                    = statuses_count = favourites_count = user_created_at = bi_followers_count = ''
            if hasattr(post2json, 'geo'):
                if hasattr(post2json['geo'], 'coordinates'):
                    geo_lng = post2json['geo']['coordinates'][0]
                    geo_lat = post2json['geo']['coordinates'][1]
            else:
                geo_lng = ''
                geo_lat = ''
            if hasattr(post2json, 'retweeted_status'):
                retweeted_status = post2json['retweeted_status']
            else:
                retweeted_status = ''
            if hasattr(post2json, 'reposts_count'):
                reposts_count = post2json['reposts_count']
            else:
                reposts_count = ''
            if hasattr(post2json, 'comments_count'):
                comments_count = post2json['comments_count']
            else:
                comments_count = ''
            if hasattr(post2json, 'attitudes_count'):
                attitudes_count = post2json['attitudes_count']
            else:
                attitudes_count = ''
            mysql_connection.insert(mysql_weibodata,
                                    id=pid,
                                    created_at=created_at,
                                    text=text,
                                    uid=uid,
                                    geo_lng=geo_lng,
                                    geo_lat=geo_lat,
                                    retweeted_status=retweeted_status,
                                    reposts_count=reposts_count,
                                    comments_count=comments_count,
                                    attitudes_count=attitudes_count)
            mysql_connection.insert(mysql_weibouser,
                                    uid=uid,
                                    province=province,
                                    city=city,
                                    location=location,
                                    gender=gender,
                                    followers_count=followers_count,
                                    friends_count=friends_count,
                                    statuses_count=statuses_count,
                                    favourites_count=favourites_count,
                                    created_at=user_created_at,
                                    bi_followers_count=bi_followers_count)
            mysql_connection.commit()
            count += 1
            curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if count % 100 == 0:
                print '%s----->%s/%s<------' % (curtime, str(count), str(total))
        curtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print '%s----->%s dealed' % (curtime, collection)
    print 'all record finished'