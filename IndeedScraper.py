from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set home url and setup driver
home_url = 'https://www.indeed.com'
url = 'https://www.indeed.com/browsejobs/Title/A'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Use Selenium to get HTML for BS4
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Create Blank list for starting_letter links
starting_letter_links = list()
# Grab all Links based on starting Letter
starting_letter_half_links = soup.find_all('a', {'class': 'text_level_3'})
# add links to list
for starting_letter_half_link in starting_letter_half_links:
    starting_letter_link = starting_letter_half_link.attrs['href']
    starting_letter_link = home_url + str(starting_letter_link)
    starting_letter_links.append(starting_letter_link)

# sort to grab only starting letter links
starting_letter_links.sort()
starting_letter_links = starting_letter_links[:26]
# print(starting_letter_links)
# create blank list for job group title links
job_group_links = list()
#
# Grab URL for each Job Group
for starting_letter_link in starting_letter_links:
    driver.get(starting_letter_link)
    html1 = driver.page_source
    soup1 = BeautifulSoup(html1, 'html.parser')
    half_links1 = soup1.find_all('a', {'class': 'jobTitle text_level_3'})
    for half_link1 in half_links1:
        job_group_link = half_link1.attrs['href']
        job_group_links.append(job_group_link)

# Save list to csv for faster testing
df = pd.DataFrame(job_group_links, columns=['Job Group URL'])
df.to_csv('job_group_url.csv')

df = pd.read_csv('job_group_url.csv')
job_group_links = df['Job Group URL'].tolist()
no_of_jobs = list()
no_of_pages = list()
group_titles = list()
# Open Each Job Group
for job_group_link in job_group_links:
    driver.get(home_url+job_group_link)
    print('URl: ' + str(home_url+job_group_link))
    # Get the number of Jobs and Pages
    job_group_link_html = driver.page_source
    job_group_link_html_soup = BeautifulSoup(job_group_link_html, 'html.parser')
    group_title = job_group_link_html_soup.find('meta', attrs={'name': 'keywords'})
    group_title = str(group_title).replace('"', ',').split(',')[1]
    group_title = group_title.split(' Jobs')[0]
    group_titles.append(group_title)
    no_of_job = job_group_link_html_soup.find('meta', attrs={'name': 'description'})
    try:
        no_of_job = int(str(no_of_job).replace('"', ' ').split(' ')[2].replace(',',''))
    except ValueError:
        no_of_job = 0
    no_of_jobs.append(no_of_job)
    no_of_page = no_of_job/15
    no_of_pages.append(no_of_page)

df = pd.DataFrame(list(zip(job_group_links, group_titles,no_of_jobs, no_of_pages)), columns=['url', 'title', 'jobs', 'pages'])
df.to_csv('job_group_details.csv')

