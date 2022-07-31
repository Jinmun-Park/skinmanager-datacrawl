"""
https://wookidocs.tistory.com/121
https://gorokke.tistory.com/20
https://thenicesj.tistory.com/128?category=1055761
"""

# Schedule
import time
# Crawling
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# Data
import pandas as pd
# Config
import json


with open('config/config.json', 'r') as f:
    config = json.load(f)

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def switch_iframe():
    try:
        driver.switch_to.frame("cafe_main")
    except:
        pass

driver = set_chrome_driver()

# STEP 1 : URL
naver_url = 'https://nid.naver.com/nidlogin.login'
# NAVER URL
blog_name = 'imsanbu'
blog_url = 'https://cafe.naver.com/' + blog_name
# NAVER ID & PW
id = config['id']
pw = config['pw']

driver.get(naver_url)
driver.implicitly_wait(3)

driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")
driver.find_element('xpath', '//*[@id="log.login"]').click()
time.sleep(3)

driver.get(blog_url)
driver.implicitly_wait(3)

driver.find_element('name', 'query').send_keys('??')
driver.find_element('name', 'query').send_keys(Keys.ENTER)
time.sleep(3)

switch_iframe()

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
soup = soup.find_all(class_='article-board result-board m-tcol-c')[0]

td_article = soup.find_all(class_='td_article')
td_date = soup.find_all(class_='td_date')
td_view = soup.find_all(class_='td_view')

#article_date = soup.find_all(class_='td_date')[0]
#article_date = td_date.get_text().strip()
#article_view = soup.find_all(class_='td_view')[0]
#article_view = article_view.get_text().strip()



new_df = pd.DataFrame(columns=['title', 'date', 'views'])
#new_df = new_df.concat({'title': article_title, 'date': article_date, 'views': article_view},ignore_index=True, axis=0)
#new_df = pd.concat([new_df, pd.DataFrame.from_records([{'title': article_title, 'date': article_date, 'views': article_view}])], ignore_index=True)

for article, date, view in zip(td_article, td_date, td_view):

    article_title = article.find(class_='article')
    article_title = article_title.get_text().strip()
    #link = article_title.get('href')

    article_date = date.get_text().strip()

    article_view = view.get_text().strip()

    new_df = pd.concat([new_df, pd.DataFrame.from_records([{'title': article_title, 'date': article_date, 'views': article_view}])], ignore_index=True)




#main-area > div.article-board.result-board.m-tcol-c > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a.article
#main-area > div.article-board.result-board.m-tcol-c > table > tbody > tr:nth-child(14) > td.td_article > div.board-list > div > a.article

titles = soup.select("main-area > div.article-board.result-board.m-tcol-c > table > tbody > tr:nth-child(1) > td.td_article > div.board-list > div > a.article")
print("hi")

for i in range(1, 3):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select("#main-area > div:nth-child(7) > table > tbody > tr")


    print('----' + str(i) + ' ?? ??? -----')
    list3 = []

    for title in titles:
        list = title.select_one(' td.td_article > div.board-list > div > a').text
        list2 = ''.join(list.split())
        list3.append(list2)

    list4_sr = pd.Series(list3)
    print(list4_sr)

    # for a in range(1, 3):
        # driver.find_element_by_xpath(f'//*[@id="main-area"]/div[5]/table/tbody/tr[{a}]/td[1]/div[2]/div/a').click()
        # time.sleep(3)
        # driver.back()
        # time.sleep(2)
        # driver.switch_to.frame("cafe_main")
    if i<2:
        driver.find_element_by_xpath(f'//*[@id="main-area"]/div[7]/a[{i}+1]').click()
