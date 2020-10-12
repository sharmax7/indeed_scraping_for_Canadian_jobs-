#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver=webdriver.Chrome()
url = 'https://www.indeed.ca/jobs?q=python&l=Alberta&start='
data=driver.get(url)

soup=BeautifulSoup(driver.page_source, 'html.parser') #can also use 'html.parser instead of lxml'
all_info = soup.find_all('div', {'class':'jobsearch-SerpJobCard'})

page_info=soup.find('div',{'id':'searchCountPages'}).text.replace("\n","").strip(" ").split(" ")
my_string=page_info[3]
total_jobs=int(my_string.replace(",",""))
#no_of_pages=total_jobs/15
#rounded_no_of_pages=round(no_of_pages) 

l=[]
for page in range(0,total_jobs,10):
    link = url+str(page)
    print(link)
    data=driver.get(link)
    #load data in to bs4
    time.sleep(10)
    soup=BeautifulSoup(driver.page_source, 'html.parser') #can also use 'html.parser instead of lxml'
   # page_info=find('div',{'class':'secondRow'})
    all_info = soup.find_all('div', {'class':'jobsearch-SerpJobCard'})

    for information in all_info:
        d={}
        try:
            d['title'] = information.find('h2',{'class':'title'}).text.strip()
        except:
            d['title'] = None
        try:
            d['company'] = information.find('div', {'class':'sjcl'}).find('span',{'class':'company'}).text.strip()
        except:
            d['company']=None

        try:
            d['ratings']= information.find('div', {'class':'sjcl'}).find('span',{'class':'ratingsDisplay'}).text.strip()
        except:
            d['ratings']=None
        try:
            d['location'] = information.find('div', {'class':'sjcl'}).find('span',{'class':'location accessible-contrast-color-location'}).text.strip()
        except:
            d['Location']=None

        l.append(d)

df=pd.DataFrame(l)
df


df.to_csv("indeed_data12.csv")

