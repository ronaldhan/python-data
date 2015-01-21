# -*- coding:utf-8 -*-
import pymongo
import python_mysql as mydb

from weibodataconfig import *


if __name__ == '__main__':
    mongo_connection = pymongo.Connection(mongo_host, mongo_port)
    mysql_connection = mydb.Connection(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)