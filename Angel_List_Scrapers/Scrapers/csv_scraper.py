
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium')


# In[2]:


get_ipython().system('pip install bs4')


# In[3]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import bs4
from bs4 import BeautifulSoup
import re


# In[6]:


# Function for opening the WebDriver, scrolling for max page view, and then capturing the html
def FFwebdriver(driver):
    time.sleep(10)
    pause = 3

    try:
         lastHeight = driver.execute_script("return document.body.scrollHeight")
    except:
        return None

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        try:
            driver.find_element_by_class_name('more').click()
        except:
            break
        time.sleep(pause)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight

    time.sleep(pause)
    htmlResults = driver.page_source

    return htmlResults


# In[25]:


def csv_scrape(csv):
    
    #list to return
    descriptions = []
    
    #initialize webdriver
    driver=webdriver.Firefox(executable_path='C:/Users/Daricus/Downloads/geckodriver-v0.24.0-win64/geckodriver.exe')
    
    #turn raw csv from github into dataframe for ease
    df = pd.read_csv(csv)
    
    #conditionally searches angellist for products with taglines and extracts the blobs
    for x in range(len(df)):
        if df['tagline'][x] !="Empty section for this company":
            url = df.AngelList_website[x]
            driver.get(url)
            html = FFwebdriver(driver)
            html = bs4.BeautifulSoup(html)
            html2 = html.find(class_="new_product section")
            desc = html2.text
            desc = desc.strip()
            descriptions.append(desc)
    return descriptions


# In[26]:


descriptions_list = csv_scrape('https://raw.githubusercontent.com/veritaem/DS-Sprint-01-Dealing-With-Data/master/angel-co-1000000-100000000.csv')
descriptions_list

