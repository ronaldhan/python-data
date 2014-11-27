# -*- coding:utf-8 -*-
import requests
import time


tcount = 5
firstrUrl = 'www.baidu1111111.com'
firstPage = 'x'


def getpage():
    global tcount
    global firstrUrl
    global firstPage
    try:
        fPage = requests.get(firstrUrl)
        if fPage.status_code == 200:
            firstPage = fPage.text
            return firstPage
    except Exception,ex:
        value='1'
        if  tcount:
            stime = 1*(6 - tcount)
            print '将等待%s秒，第%s次重试……' % (str(stime), str(6 - tcount))
            time.sleep(stime)
            tcount -= 1
            value=getpage()
            return value
        else:
            print 'all'
            return '2'

if __name__ == '__main__':
   value=getpage()
   print value

        
