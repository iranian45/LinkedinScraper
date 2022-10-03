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

home_url = 'https://www.indeed.com'
url = 'https://www.indeed.com/browsejobs/Title/A'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Uses Selenium to grab html code to use with BS4
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# print(soup)

links = set()
half_links = soup.find_all('a', {'class': 'text_level_3'})

# Grabs URL for each Job Title Starting Letter
for half_link in half_links:
    link = half_link.attrs['href']
    links.add(link)

links_list = list(links)
links_list.sort()
alphabet_links = links_list[:26]

# For each letter go in and grab Each Job Title and save to CSV
for link in alphabet_links:
    # Uses Selenium to grab html code to use with BS4
    driver.get(home_url + link)
    time.sleep(10)
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    # BS4 Grabs
    half_links1 = soup1.find_all('a', {'class': 'text_level_3'})
    for half_link1 in half_links1:
        link1 = half_link1.attrs['href']
        links.add(link1)

links_list = list(links)
links_list.sort()
title_links = links_list[26:]
df = pd.DataFrame(title_links, columns=['Title_Links'])
df.to_csv('title_links.csv', index=False)

# Load CSV for Job Title links
links2 = set()
df1 = pd.read_csv('title_links.csv')
title_links = df1.Title_Links.to_list()

# For each Title grab each Job Posting
for titlelink in title_links:

    driver.get(home_url + titlelink)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    next_link = soup.find_all('a', {'data-testid': 'pagination-page-next'})

    time.sleep(2)

    try:
        time.sleep(2)
        popup = driver.find_element(By.ID, 'popover-form-container')
        driver.find_element(By.XPATH, '//*[@id="popover-x"]/button').click()
        time.sleep(2)
        no_of_jobs = soup.find('div', {'class': 'searchCount-a11y-contrast-color'}).text.strip()
        no_of_jobs = no_of_jobs.replace(',', '')
        no_of_jobs = re.findall('\d+', no_of_jobs)
        no_of_jobs = math.floor(int(no_of_jobs[-1]) / 15)
        print('Popup')
        print(home_url + titlelink)
    except NoSuchElementException:
        time.sleep(2)
        no_of_jobs = soup.find('div', {'class': 'jobsearch-JobCountAndSortPane-jobCount'})
        no_of_jobs = no_of_jobs.find(text=True).strip().split(' ')
        no_of_jobs = no_of_jobs[-2].replace(',', '')
        no_of_jobs = math.floor(int(no_of_jobs) / 15)
        print('No Popup')
        print(home_url + titlelink)

    # print(no_of_jobs)

    url = driver.current_url
    links2 = set()

    try:
        time.sleep(2)
        popup = driver.find_element(By.ID, 'popover-form-container')
        driver.find_element(By.XPATH, '//*[@id="popover-x"]/button').click()
        time.sleep(2)

        for x in range(0, no_of_jobs, 10):
            # print(url + '&start=' + str(x))

            for link in title_links:
                driver.get(url + '&start=' + str(x))
                time.sleep(5)
                html2 = driver.page_source
                soup2 = BeautifulSoup(html2, 'html.parser')
                half_links2 = soup2.find_all('a', {'class': 'jcs-JobTitle css-jspxzf eu4oa1w0'})
                for half_links2 in half_links2:
                    link2 = half_links2.attrs['href']
                    links2.add(link2)
                    # print(half_links2)

    except NoSuchElementException:
        time.sleep(2)
        for x in range(0, no_of_jobs, 10):
            # print(url + '&start=' + str(x))

            for link in title_links:
                driver.get(url + '&start=' + str(x))
                time.sleep(5)
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

job_links = df2.job_links.to_list()

url = list()
company_name = list()
title = list()
salary = list()
salary_min = list()
salary_max = list()
location = list()
description = list()

for job_link in job_links:
    driver.get(home_url+job_link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    url.append(home_url + job_link)
    job_title = soup.find('h1', {'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
    title.append(job_title)
    sal_range = soup.find('span', {'class': 'icl-u-xs-mr--xs'})
    company = soup.find_all('div', {'class': 'icl-u-lg-mr--sm icl-u-xs-mr--xs'})[1].text
    company_name.append(company)
    location = soup.find('div', {'class': 'icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle'})
    location = str(location).split("<div>")[-1].split("<")[0]
    descrip = soup.find('div', {'class': 'jobsearch-jobDescriptionText'}).text
    description.append(descrip)

    try:
        sal_range = soup.find('span', {'class': 'icl-u-xs-mr--xs'}).text
        sal_range = sal_range.replace(',', '')
        sal_range = re.findall('\d+', sal_range)
        sal_min = sal_range[0]
        sal_max = sal_range[-1]
    except AttributeError:
        sal_range = "Null"
    salary.append(sal_range)
    salary_min.append(sal_min)
    salary_max.append(sal_max)
    time.sleep(2)

df3 = pd.DataFrame(list(zip(title, company_name, salary_min, salary_max, description, url)), columns= ['Job Title', 'Company Name', 'Salary Min', 'Salary Max', 'Job Description', 'Job Posting Url'])

df3.to_csv('F_IndeedJob.csv', index=False)

