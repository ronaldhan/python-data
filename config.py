#coding=utf8

dbPath="C:\\Program Files (x86)\\火车采集器V8\\Data\\"
fileName="SpiderResult.db3"

tables={
    '银行':'bank',
    '公司企业':'company',
    '洗衣店':'dry_cleaner',
    '医院':'hospital',
    '学校':'school',
    '培训':'training',
    '旅行社':'traveling',
    '居家维修':'maintenance',
    '房地产':'property',
    '商务楼':'bbuilding',
    '美食':'food',
    '休闲娱乐':'entertainment',
    '酒店':'hotel',
    '丽人':'figure',
    '购物':'shopping',
    '运动健身':'fitness'    
}

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

tencent_city="北京市"
tencentAPI_geocoding="http://apis.map.qq.com/ws/place/v1/search"
tencent_api_ak="46IBZ-DGRRV-LRGPO-UTXFR-RWSBT-BFFJN"
