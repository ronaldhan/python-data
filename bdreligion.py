# -*- coding:utf-8 -*-

print '输入需要划分区域的左下和右上坐标，格式如下:'
print '%s(左下纬度),%s(左下经度);%s(右上纬度),%s(右上经度)' % ('39.768', '116.06', '39.904', '116.474')
LJ = 0.0
LW = 0.0
TJ = 0.0
TW = 0.0
parts = 4
religions = {}
coors = raw_input("输入坐标:\n")
coors = '39.768,116.06;39.904,116.474'
print '输入坐标为：%s' % coors
parts = int(raw_input("输入分区数（偶数）:\n"))
print '输入分区数为%d' % parts
if parts < 4:
    parts = 4
clist = coors.split(';')
LW = float(clist[0].split(',')[0])
LJ = float(clist[0].split(',')[1])
TW = float(clist[1].split(',')[0])
TJ = float(clist[1].split(',')[1])
DJ = TJ - LJ
DW = TW - LW
for i in range(parts):
    ct = []
    if i < parts/2:
        p1 = LW
        p2 = LJ + 2*DJ*i/parts
        p3 = LW + DW/2
        p4 = LJ + 2*DJ*(i + 1)/parts
    else:
        p1 = LW + DW/2
        p2 = LJ + 2*DJ*(i - parts/2)/parts
        p3 = LW + DW
        p4 = LJ + 2*DJ*(i - parts/2 + 1)/parts
    ct.append(str(p1))
    ct.append(str(p2))
    ct.append(str(p3))
    ct.append(str(p4))
    religions[i + 1] = ct
for k, v in religions.iteritems():
    print '%d:%s' % (k, v)