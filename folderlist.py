#-*-coding:utf8-*-
import os

def get(path):
    d=os.walk(path)
    f=d.next()
    print f
    return f
	
if __name__=='__main__':
    path='C:\\Program Files (x86)\\火车采集器V8\\Data'
    d=get(path)
    print d
