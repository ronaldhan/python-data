# -*- coding:utf-8 -*-
import json

import requests

import python_mysql as mydb
from toolsconfig import *


def bd_geocoding(url=BD_API_GEOCODING, params=bd_geocoding_params):
    """
    解析获取经纬度坐标
    :param url:百度接口地址
    :param params:百度接口传入参数,包含地址
    :return:包含经纬度坐标的二元组,字符串格式
    """
    r = requests.get(url, params)
    fresult = r.json()
    if fresult['status'] == 0:
        result = fresult['result']
        if 'location' in result.keys():
            lng = str(result['location']['lng'])
            lat = str(result['location']['lat'])
    else:
        lng = ''
        lat = ''

    return lng, lat







