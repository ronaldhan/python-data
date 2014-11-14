# -*- coding:utf-8 -*-
import urllib2
from pyquery import PyQuery as pq
import urllib
import cookielib
import os

base = 'http://www.bjdata.gov.cn/'
root = 'http://www.bjdata.gov.cn/Default.aspx'
folder = r'D:\data\bjdata'
loginpage = urllib2.urlopen(root).read()
data = pq(loginpage)
viewstate = data("input[name='__VIEWSTATE']").attr('value')
values = {
    '__essVariable': {
        "dshReset_imgIcon:exp":"-1",
        "dshQuestionAnswer_imgIcon:exp":"-1",
        "__scdoff":"1",
        "__ess_pageload":"__ess_SetInitialFocus(\u0027ess_ctr410_ViewGeneralModule_ctl00_essSIGNIN_Login_ESS_txtUsername\u0027);"
    },
    'ess$ctr410$ViewGeneralModule$ctl00$essSIGNIN$Login_ESS$txtUsername': 'ronald',
    'ess$ctr410$ViewGeneralModule$ctl00$essSIGNIN$Login_ESS$txtPassword': 'HZH1988',
    'ess$ctr410$ViewGeneralModule$ctl00$essSIGNIN$Login_ESS$cmdLogin': '登录',
    '__VIEWSTATE': viewstate
}
#设置cookie信息
pdata = urllib.urlencode(values)
jar = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(jar)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
#获取登陆后状态
req = urllib2.Request(root, pdata)
loggedpage = urllib2.urlopen(req).read()
url = 'http://www.bjdata.gov.cn/tabid/68/Default.aspx?cid=26371'
#有cookie信息后，postdata信息就不需要了
# req = urllib2.Request(url, pdata)
# filepage = urllib2.urlopen(req).read()
filepage = urllib2.urlopen(url).read()
pagedata = pq(filepage)
kinds = pagedata('td .NodeStyle')
#文件计数
count = 1
kcount = 1
#共有17类
for kind in kinds:
   rurl = kind.values()[1]
   rpage = urllib2.urlopen(rurl).read()
   rdata = pq(rpage)
   trs = rdata('tr .item')
   for tr in trs:
       tr = pq(tr)
       #'http://www.bjdata.gov.cn/tabid/93/Default.aspx?did=239'
       kurl = tr('a').attr('href')
       #url的查询参数为下载地址对应的参数
       num = kurl[kurl.rindex('=')+1:]
       durl = base + 'download.aspx?did=' + num
       zipfile = urllib2.urlopen(durl).read()
       fname = str(count) + '.zip'
       filepath = os.path.join(folder, fname)
       with open(filepath, 'wb') as code:
           code.write(zipfile)
       count = count + 1
       print '%s had finished' % str(num)
   print '=====%s kind had finished=====' % str(kcount)
   kcount = kcount + 1
print '!!!-->download finished<--!!!'
