#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import urllib2
import re
import time
#import string

def get_page():
    try:
        url=urllib2.Request('http://jwc.ncepubd.edu.cn/m/Home/Notice')
        r=urllib2.urlopen(url).read()
        #r= r.translate(None,string.punctuation)
        #print r
        return r
    except:
        print 'have an error'
        
def get_new_notice(r):
    pattern = r'h2>([\s\S]*?)</h2>[\s\S]*?<p>([\s\S]*?)</p'
    Notice=re.findall(pattern,r)
    try:    
        fhand = open(r'/storage/sdcard0/notice.txt','r')  
    except:
        return Notice 
    old_notice=eval(fhand.read())
    new_notice=list()
    dic=dict()
    for key,value in Notice[0:-1]:
        if key in old_notice: continue
        new_notice.append((key,value))
    if len(new_notice) > 0:
        for (i,j) in new_notice:
            print i+j
        return Notice
    else :
        return False


def save_to_file(Notice):
    dic = dict()
    with open(r'/storage/sdcard0/notice.txt','w') as fhand:
        for notice,day in Notice[0:-1]: 
            dic[notice]=day        
        fhand.write(str(dic))
    print '保存新文件'

if __name__ == '__main__':
    while True:
        r = get_page()
        Notice = get_new_notice(r)
        if Notice:
            save_to_file(Notice)
        else:
            print 'NO new notice!'
        time.sleep(300)