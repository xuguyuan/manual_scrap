# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 18:09:23 2018

@author: weiping
"""


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
html = urlopen('http://www.shenzhong.net/news_24/5888.html')
bsObj = BeautifulSoup(html)


nameList2 = bsObj.findAll("div",{"class":"wqptable-box"})
nameList3 = bsObj.findAll("table",{"width":"512"})
nameList = bsObj.findAll("tr",{"style":";height:27px"})
         
string.index(',')


# this is for test
#this is for test 2
        
        
    

