from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import math
import pandas as pd
import time


df1 = pd.read_csv('title_links.csv')
title_links = df1.Title_Links.to_list()

home_url = 'https://www.indeed.com'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for titlelink in title_links:

    driver.get(home_url+titlelink)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find_all('a', {'data-testid': 'pagination-page-next'})

    try:
        time.sleep(1)
        popup = driver.find_element(By.ID, 'popover-form-container')
        driver.find_element(By.XPATH, '//*[@id="popover-x"]/button').click()
        time.sleep(1)
        no_of_jobs = soup.find('div', {'class': 'searchCount-a11y-contrast-color'}).text.strip()
        no_of_jobs = no_of_jobs.replace(',', '')
        no_of_jobs = re.findall('\d+', no_of_jobs)
        no_of_jobs = math.floor(int(no_of_jobs[-1])/15)
        print('Popup')
        
    except NoSuchElementException:
        time.sleep(1)
        no_of_jobs = soup.find('div', {'class': 'jobsearch-JobCountAndSortPane-jobCount'})
        no_of_jobs = no_of_jobs.find(text=True).strip().split(' ')
        no_of_jobs = no_of_jobs[-2].replace(',', '')
        no_of_jobs = math.floor(int(no_of_jobs)/15)
        print('No Popup')

    print(no_of_jobs)

    url = driver.current_url
    links2 = set()

    try:
        time.sleep(1)
        popup = driver.find_element(By.ID, 'popover-form-container')
        driver.find_element(By.XPATH, '//*[@id="popover-x"]/button').click()
        time.sleep(1)

        for x in range(0, no_of_jobs, 10):
            print(url+'&start='+str(x))

            for link in title_links:
                driver.get(url+'&start='+str(x))
                time.sleep(5)
                html2 = driver.page_source
                soup2 = BeautifulSoup(html2, 'html.parser')
                half_links2 = soup2.find_all('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'})
                for half_links2 in half_links2:
                    link2 = half_links2.attrs['href']
                    links2.add(link2)
                    # print(half_links2)

    except NoSuchElementException:
        time.sleep(1)
        for x in range(0, no_of_jobs, 10):
            print(url + '&start=' + str(x))

            for link in title_links:
                driver.get(url + '&start=' + str(x))
                time.sleep(1)
                html2 = driver.page_source
                soup2 = BeautifulSoup(html2, 'html.parser')
                half_links2 = soup2.find_all('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'})
                for half_links2 in half_links2:
                    link2 = half_links2.attrs['href']
                    links2.add(link2)
                    # print(half_links2)

links2_list = list(links2)
links2_list.sort()
df2 = pd.DataFrame(links2_list, columns=['job_links'])
df2.to_csv('joblinks.csv', index=False)


