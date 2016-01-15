#-*-coding:utf8;-*-
#qpy:2
#qpy:console

import urllib2
import re
import time

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
    lst = list()
    notice_list = list()
    have_new_notice = False
    for i,j in Notice:
        lst.append(i+j)
    fin = open(r'notice.txt','r')
    for notice in fin.readline():
        if notice not in lst:
            have_new_notice = True
            notice_list.append(notice)
    fin.close()
    return lst,notice_list,have_new_notice

def sve_to_file(have_new_notice):
    if have_new_notice:
        fhand = open(r'notice.txt','w')
        for tice in lst:
            fhand.write(i+j+'\n')
        fhand.close()


    

if __name__ == '__main__':
    
    r = get_page()
    get_new_notice(r)