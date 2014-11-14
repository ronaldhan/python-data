# -*- coding:utf-8 -*-
import urllib2
import urllib
import json
import shapefile as shp
from decimal import Decimal
import os
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

bd = 'http://api.map.baidu.com/geoconv/v1/?'
ak = 'UjDN5L4WOmeoTAMIZG73MU1F'
myfile = r'C:\Users\sony\Desktop\test\ftb.txt'
rpath = r'C:\Users\sony\Desktop\test'
filename = 'ftbound'
txt = open(myfile, 'r')
a = txt.read()
b = a.split(',')
count = 0
r = ''
for item in b:
    if count < len(b) - 1:
        if count > 0 and count % 2 != 0:
            r = r + item + ';'
        else:
            r = r + item + ','
    else:
        r = r + item
    count = count + 1

content = r.split(';')
index = 0
wdata = [0]
# fdata = [0 for col in range(len(content))]
# tmp = [0 for col in range(2)]
params = {
    'from': 6,
    'to': 5,
    'ak': ak
}
w = shp.Writer(shp.POINT)
w.field('id', 'C', '8')
for point in content:
    params['coords'] = point
    rURL = bd + urllib.urlencode(params)
    print rURL
    data = urllib2.urlopen(rURL).read()
    result = json.loads(data)
    pxpy = result['result']
    # tmp[0] = pxpy[0]['x']
    # tmp[1] = pxpy[0]['y']
    # print tmp
    # fdata[index] = tmp
    index += 1
    w.point(pxpy[0]['x'], pxpy[0]['y'])
    w.record(str(index))
# wdata[0] = fdata
# print wdata
# w = shp.Writer(shp.POLYLINE)
# w.field('id', 'C', '8')
# w.poly(parts=wdata)
# w.record('0')
shape = StringIO()
shx = StringIO()
dbf = StringIO()
w.saveDbf(os.path.join(rpath, filename))
w.saveShp(os.path.join(rpath, filename))
w.saveShx(os.path.join(rpath, filename))
print '%s had created' % filename


