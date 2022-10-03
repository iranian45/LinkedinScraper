from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


home_url = 'https://www.indeed.com'
url = 'https://www.indeed.com/browsejobs/Title/A'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

links = set()
half_links = soup.find_all('a', {'class': 'text_level_3'})

for half_link in half_links:
    link = half_link.attrs['href']
    links.add(link)

links_list = list(links)
links_list.sort()
alphabet_links = links_list[:26]

for link in alphabet_links:
    driver.get(home_url+link)
    time.sleep(10)
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    half_links1 = soup1.find_all('a', {'class': 'text_level_3'})
    for half_link1 in half_links1:
        link1 = half_link1.attrs['href']
        links.add(link1)

links_list = list(links)
links_list.sort()
title_links = links_list[26:]
df = pd.DataFrame(title_links, columns=['Title_Links'])
df.to_csv('title_links.csv', index=False)

links2 = set()
df1 = pd.read_csv('title_links.csv')
title_links = df1.Title_Links.to_list()


for link in title_links:
    driver.get(home_url+link)
    time.sleep(30)
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2, 'html.parser')
    half_links2 = soup2.find_all('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'})
    for half_links2 in half_links2:
        link2 = half_links2.attrs['href']
        links2.add(link2)



links2_list = list(links2)
links2_list.sort()
df2 = pd.DataFrame(links2_list, columns=['job_links'])
df2.to_csv('joblinks.csv', index=False)

# Job Title class is 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'
# Job Description class is 'jobsearch-jobDescriptionText'
# next page attr is 'data-testid="pagination-page-next"'
