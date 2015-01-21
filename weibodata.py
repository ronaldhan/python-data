# -*- coding:utf-8 -*-
import json

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
        for post in user_collction.find():
            post2json = json.loads(post)
            if hasattr(post2json, 'id'):
                id = post2json['id']
            else:
                id = ''
            if hasattr(post2json, 'created_at'):
                created_at = post2json['created_at']
            else:
                created_at = ''
            if hasattr(post2json, 'text'):
                text = post2json['text']
            else:
                text = ''
            if hasattr(post2json, 'user'):
                if hasattr(post2json['user'], 'id'):
                    uid = post2json['user']['id']
            else:
                uid = ''
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
            if hasattr(post2json, 'repost_count'):
                repost_count = post2json['repost_count']
            else:
                repost_count = ''
            if hasattr(post2json, 'comments_count'):
                comments_count = post2json['comments_count']
            else:
                comments_count = ''
            if hasattr(post2json, 'attitudes_count'):
                attitudes_count = post2json['attitudes_count']
            else:
                attitudes_count = ''