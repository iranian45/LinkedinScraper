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

df2 = pd.read_csv('joblinks.csv')
job_links = df2.job_links.to_list()

home_url = 'https://www.indeed.com'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

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
pd.set_option('display.max_columns', None)
print(df3.head(15))
