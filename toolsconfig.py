# -*- coding:utf-8 -*-
# 百度地图API
# 地点详情查询接口
BD_API_DETAIL = 'http://api.map.baidu.com/place/v2/detail?'
# 地理坐标转换接口
BD_API_GEOCONV = 'http://api.map.baidu.com/geoconv/v1/?'
# 地点查询接口
BD_API_PLACE = 'http://api.map.baidu.com/place/v2/search?'
# 地址解析和逆地址解析接口
BD_API_GEOCODING = 'http://api.map.baidu.com/geocoder/v2/?'
# 接口需要的密钥
BD_API_AK = 'UjDN5L4WOmeoTAMIZG73MU1F'

# BD_API_PLACE接口查询默认参数
bd_place_params = {
    'output': 'json',
    'ak': BD_API_AK,
    'page_num': '0',
    'page_size': '20'
}

# BD_API_DETAIL 接口默认参数
bd_detail_params = {
    'output': 'json',
    'ak': BD_API_AK,
    'scope': '2'
}

# BD_API_GEOCODING 接口默认参数
bd_geocoding_params = {
    'ak': BD_API_AK,
    'output': 'json'
}

# 腾讯地图API
# 地址解析和逆地址解析接口
TX_API_PLACE = 'http://apis.map.qq.com/ws/place/v1/search?'
# 接口需要的密钥
TX_API_AK = '46IBZ-DGRRV-LRGPO-UTXFR-RWSBT-BFFJN'

# TX_API_PLACE接口查询默认参数
tx_palce_params = {
    'key': TX_API_AK
}


# 网络坐标转WGS坐标接口
BD2WGS = 'http://api.zdoz.net/bd2wgs.aspx?'

# mysql默认参数
mysql_host = "localhost"
mysql_user = "root"
mysql_password = "ronald"
mysql_port = 3306

# mongo默认参数
mongo_host = "localhost"
mongo_port = 27017