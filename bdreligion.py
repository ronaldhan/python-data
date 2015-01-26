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
print '分区模式，格式: %s(横行)*%s(纵行)'
parts = raw_input("输入分区模式:\n")
# todo 对输入的模式通过正则表达式进行判断，满足'整数*整数'的模式
if '*' in parts:
    part = parts.split('*')
    XP = part[0]
    YP = part[1]
else:
    print '输入模式有误'
clist = coors.split(';')
LW = float(clist[0].split(',')[0])
LJ = float(clist[0].split(',')[1])
TW = float(clist[1].split(',')[0])
TJ = float(clist[1].split(',')[1])
DJ = TJ - LJ
DW = TW - LW
count = 0

for i in range(YP):
    for j in range(XP):
        ct = []
        p1 = LW + i*DW/YP
        p2 = LJ + j*DJ/XP
        p3 = LW + (i + 1)*DW/YP
        p4 = LJ + (j + 1)*DJ/XP
        ct.append(str(p1))
        ct.append(str(p2))
        ct.append(str(p3))
        ct.append(str(p4))
        count += 1
        religions[count] = ct
for k, v in religions.iteritems():
    print '%d:%s' % (k, v)