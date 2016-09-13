# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from requests import Session
import re
import sqlite3
import time
import sys
from user_config import UserName,Password
# import weixin
import sendemail

reload(sys)
sys.setdefaultencoding('utf-8')

class NoticeSpider():
    """docstring for NoticeSpider"""
    def __init__(self):
        self.s = Session()
        self.conn = sqlite3.connect('ntice_v1.1.sqlite')
        self.cur = self.conn.cursor()
        self.notice_url = 'http://59.67.225.73/m/Home/NoticeDetail?uid='
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Notices
    (id   INTEGER  PRIMARY KEY AUTOINCREMENT ,  header TEXT UNIQUE, notice_url TEXT, noticedetail TEXT,times TEXT)''')

    def login(self):
        login_url = r'http://59.67.225.73/m/Account/Login'
        try:
            r = self.s.get(login_url)
            bsObj = BeautifulSoup(r.text, 'html.parser')
            value = bsObj.find('input').get('value')
            payload = {'__RequestVerificationToken': value,
                        'UserName':UserName,
                        'Password':Password,
                        'RememberMe':'false'
                    }
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                        'Referer': 'http://59.67.225.73/m/Account/Login',
                        'Host': '59.67.225.73',
                        'Origin': 'http://59.67.225.73',
                    }
            self.s.post(login_url, data=payload, headers=headers)
        except:
            pass


    def get_new_notice(self):
        self.login()
        try: 
             self.notice_content = self.s.get('http://59.67.225.73/m/Home/Notice').text
        except:
             print 'have an error'
        self.get_notice()

    def get_notice(self):
        try:
            bsObj = BeautifulSoup(self.notice_content, 'html.parser')
            
            notices = bsObj.find_all(href=re.compile('#'))
            for notice in notices:
                if notice.find('h2'):
                    self.times = notice.find('p').text
                    data_uid = notice.get('data-uid')
                    self.data_url = self.notice_url + data_uid
                    # notice_list[notice.find('h2').text] = self.s.get(self.data_url).text

                    self.content = self.s.get(self.data_url).text
                    bsObj = BeautifulSoup(self.content,'html.parser')
                    self.header = bsObj.find(class_='h1n').text
                    self.noticedetail = bsObj.find(id="noticedetail").text  
                    # print self.noticedetail
                    self.save_to_database()
                    time.sleep(10)
            self.conn.commit()
            self.conn.close()
        except:
            pass

    def save_to_database(self):
        self.cur.execute('SELECT header FROM Notices WHERE header = ? LIMIT 1 ',(self.header,))
        try:
            row =self.cur.fetchone()[0]
            print 'No new notice'
        except:
           # print self.header
            self.cur.execute('''INSERT INTO Notices VALUES (?,?,?,?,?)''', (None,self.header,self.data_url,self.content,self.times))
            send_text = self.header+'\n'+self.noticedetail
            # sign = weixin.send_msg(self.header)
            sendemail.sendemail('<notice>'+self.header,self.noticedetail,to_list = sendemail.TO_LIST)
            time.sleep(4)
            sendemail.sendemail(self.header,self.content,to_list = sendemail.TO_LIST1)


            
        

if __name__ == '__main__':
    print 'hello, i am here'
    spider = NoticeSpider()
    i = 0
    while 1:
        print i
        i += 1
        spider.get_new_notice()
        time.sleep(60)
    
