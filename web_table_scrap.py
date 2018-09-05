# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 18:09:23 2018

@author: weiping
"""




from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
from requests_html import HTMLSession
from pandas import DataFrame as DF
import sys
sys.setrecursionlimit(10000)



class login:

    def __init__(self, identification, password):
        #self.identification = identification
        #self.password = password
        self.post_url = 'http://210.42.121.241/servlet/Login'
        self.yzm_url = 'http://210.42.121.241/servlet/GenImg'

        self.Code = ''
        self.login_data = {'id': identification,
                      'pwd': password,#不清楚教务的表单加密方式是否会改变，需要到教务系统去核实
                      'xdvfb': ''}
        self.yam_headers ={
    #    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    #    'Accept-Encoding': 'gzip, deflate',
    #    'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
    #    'Cache-Control': 'no-cache',
    #    'Connection': 'keep-alive',
    #    'Cookie': cookies,
    #    'Host': '210.42.121.241',
    #    'Pragma': 'no-cache',
    #    'Referer': 'http://210.42.121.241/servlet/Login',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'}
        self.login_headers = {
    #    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #    'Accept-Encoding': 'gzip, deflate',
    #    'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
    #    'Cache-Control': 'no-cache',
    #    'Connection': 'keep-alive',
    #    'Content-Length': '63',
    #    'Content-Type': 'application/x-www-form-urlencoded',
    #    'Cookie':'userLanguage=zh-CN; sto-id-20480=IEHJCKNCFAAA; JSESSIONID=0FCFB70E2B7C2CCE756C9A7736E580CC.tomcat2',
    #    'Host': '210.42.121.241',
    #    'Origin': 'http://210.42.121.241',
    #    'Pragma': 'no-cache',
    #    'Referer': 'http://210.42.121.241/servlet/Login',
    #    'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'}
        #self.session = requests.session()
        self.session = HTMLSession()
    def log(self):
        yamdata = self.session.get(self.yzm_url, headers=self.yam_headers)  # receive verification code
        tempIm = BytesIO(yamdata.content)  # 将数据流放入tempIm以字节的形式
        im = Image.open(tempIm)  # 转换为图片的形式
        im.show()  # 展示验证码
        self.Code = input('Please Enter Code:')
        self.login_data['xdvfb'] = self.Code
        d = self.session.post(self.post_url, data=self.login_data, headers=self.login_headers)
        d_html = BeautifulSoup(d.text,'lxml')
        print(d_html.find("span",{"id":"term"}).get_text())
    def query(self,url,html=False):
        if html == True:
            return self.session.get(url)
        store = self.session.get(url)
        store = BeautifulSoup(store.content,'lxml')
        return store
    
    def scrap_table(self,url):
        query_content_html = admin.query(url,html = True)
        query_content = admin.query(url)
        
        trs = query_content.find_all('tr')
        trs_div = query_content_html.html.find('div')
        
        ulist = []
        for tr in trs:
            ui = []
            for td in tr:
                ui.append(td)
            ulist.append(ui)
        
        #添加了扒课程信息的功能，但是剩余/最大人数、备注等html类格式有问题，暂时还没有解决
        #已经解决
        # 3 5 7 9 11 13 15 17 19 21 23 
        # 1 3 5 7 9 11 13 15 17 19 21
        #initialize
        lessons_dict = {}
        for i in [3,5,7,9,11,13,15,17,19,21,23]:
            lessons_dict[ulist[0][i].text]=[]
        #attaching data
        for j in range(1,len(ulist)):
            for i in [3,5,7,9,11,13,15,17,19]:#,21,23]:
                lessons_dict[ulist[0][i].text].append(ulist[j][i-2].text)
            lessons_dict[ulist[0][21].text].append(trs_div[2*j].text)
            lessons_dict[ulist[0][23].text].append(trs_div[2*j+1].text)
        df = DF.from_dict(lessons_dict,orient = 'index').T
        return df
        

admin = login('2015301580264','d8bf7006acaf9cd32ae5a6c7e55c49d8')
admin.log()




url = 'http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=18'

lessons_table = admin.scrap_table(url)

#成绩单地址：http://210.42.121.241/servlet/Svlt_QueryStuScore?csrftoken=26795a33-bcc3-33c8-b55b-be3146fbaf49&year=0&term=&learnType=&scoreFlag=0&t=Wed%20Sep%2005%202018%2020:01:51%20GMT+0800%20(%D6%D0%87%F8%98%CB%9C%CA%95r%E9g)







#attach data

#c = test.session.get('http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=22')
#
#soup = BeautifulSoup(c.content,'lxml')
#test = soup.find("table",{"class":""})
#for child in soup.find("table",{"class":"table listTable"}).tr:
#    print(child)




'''
def login(identification,password):
    post_url = 'http://210.42.121.241/servlet/Login'
    yzm_url = 'http://210.42.121.241/servlet/GenImg'
    session = requests.session()  # 建立会话，保持会话信息，cookies
    r = session.get(post_url)
    #cookies = cookies.strip('; Path=/, sto-id-20480=IEHJCKNCFAAA; Expires=Mon, 28-Aug-2028 05:25:19 GMT; Path=/')  
    
    yam_headers = {
    #    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    #    'Accept-Encoding': 'gzip, deflate',
    #    'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
    #    'Cache-Control': 'no-cache',
    #    'Connection': 'keep-alive',
    #    'Cookie': cookies,
    #    'Host': '210.42.121.241',
    #    'Pragma': 'no-cache',
    #    'Referer': 'http://210.42.121.241/servlet/Login',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
            }

    
    
    
    
    
    #
    
    yamdata = session.get(yzm_url, headers=yam_headers)  # receive verification code
    tempIm = BytesIO(yamdata.content)  # 将数据流放入tempIm以字节的形式
    im = Image.open(tempIm)  # 转换为图片的形式
    im.show()  # 展示验证码

    Code = input('Please Enter Code:')
    login_data={'xdvfb':''}
    login_data['id']=identification
    login_data['pwd']=password
    login_data['xdvfb'] = Code
    login_headers = {
    #    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #    'Accept-Encoding': 'gzip, deflate',
    #    'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7',
    #    'Cache-Control': 'no-cache',
    #    'Connection': 'keep-alive',
    #    'Content-Length': '63',
    #    'Content-Type': 'application/x-www-form-urlencoded',
    #    'Cookie':'userLanguage=zh-CN; sto-id-20480=IEHJCKNCFAAA; JSESSIONID=0FCFB70E2B7C2CCE756C9A7736E580CC.tomcat2',
    #    'Host': '210.42.121.241',
    #    'Origin': 'http://210.42.121.241',
    #    'Pragma': 'no-cache',
    #    'Referer': 'http://210.42.121.241/servlet/Login',
    #    'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
    }
    

    d = session.post(post_url, data=login_data, headers=login_headers)
    d_html = BeautifulSoup(d.text,'lxml')
    print(d_html.find("span",{"id":"term"}).get_text())
    return session





login('2015301580264','d8bf7006acaf9cd32ae5a6c7e55c49d8')
'''




# this is for test
#this is for test 2
        
        
    


'''
from bs4 import BeautifulSoup
import requests
import lxml


url = 'http://www.shenzhong.net/news_24/5888.html'
web_data = requests.get(url)
# 设为utf-8编码，预防乱码
web_data.encoding = 'utf-8'
#print(web_data.text)
soup = BeautifulSoup(web_data.text, 'html.parser')
soup
sel = '/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/div/table/tbody/tr[2]/td[4]/p'
content = soup.select(sel)






from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=21')
bsObj = BeautifulSoup(html)


nameList2 = bsObj.findAll("div",{"class":"wqptable-box"})
nameList3 = bsObj.findAll("table",{"width":"512"})
nameList = bsObj.findAll("tr",{"style":";height:27px"})
nameList = bsObj.findAll("tbody")
nameList[0].get_text()


for i in range(len(nameList)):
    print(nameList[i].get_text())
string.index(',')




import urllib.request
import http.cookiejar

#/*设置文件来存储Cookie*/
filename = 'cookie.txt'
#/*创建一个MozillaCookieJar()对象实例来保存Cookie*/
cookie = http.cookiejar.MozillaCookieJar(filename)
#/*创建Cookie处理器*/
handler = urllib.request.HTTPCookieProcessor(cookie)
#/*构建opener*/
opener = urllib.request.build_opener(handler)
response = opener.open("http://210.42.121.241/stu/stu_index.jsp")
cookie.save(ignore_discard=True, ignore_expires=True)


import requests


cookie = http.cookiejar.MozillaCookieJar()
#/*加载Cookie*/
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
url = 'http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum=21'
r = requests.get(url, cookies=cookie)
print(r.text)
'''
