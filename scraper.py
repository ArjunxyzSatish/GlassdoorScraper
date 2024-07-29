#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


driver = webdriver.Firefox()

dataScience = 'https://www.glassdoor.co.uk/Job/data-science-jobs-SRCH_KO0,12.htm'
dataScientist = 'https://www.glassdoor.co.uk/Job/data-scientist-jobs-SRCH_KO0,14.htm'
dataAnalyst = 'https://www.glassdoor.co.uk/Job/data-analyst-jobs-SRCH_KO0,13.htm'
dataEngineer = 'https://www.glassdoor.co.uk/Job/data-engineer-jobs-SRCH_KO0,14.htm'

urls = [dataScience, dataScientist, dataAnalyst, dataEngineer]

jobs = []

# numJobs = 100

def loadAllJobs():

    while(True):
        try:
            more = driver.find_element(by = By.CSS_SELECTOR, value = '.JobsList_buttonWrapper__ticwb > button:nth-child(1)')
            more.click()
            time.sleep(2)
            try:
                close = driver.find_element(by = By.CSS_SELECTOR, value = '.CloseButton')
                close.click()
                print('popup closed')
            except:
                print('No poopy popup...loading more jobs...')
        except:
            print('All jobs loaded')
            break

def closeCookies():
    try:
        cookies = driver.find_element(by = By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
        cookies.click()
    except:
        print('No cookies button found')


def get_jobs(url):

    print(f'Looking for jobs in {url}')

    driver.get(url)

    time.sleep(4)

    closeCookies()

    loadAllJobs()

    job_listings = driver.find_elements(by = By.CLASS_NAME, value = 'JobCard_jobCardContainer___hKKI')

    print(len(job_listings))

    for i in range(0, len(job_listings)):
        try:
            job_listings[i].click()
            time.sleep(1)
            deets = driver.find_element(by = By.XPATH, value = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/header/div[1]').text

            lines = deets.split('\n')

            employer = lines[0]

            try:
                pattern = r'\b\d+\.\d+\b'
                rating = re.findall(pattern, deets)
                title = lines[2]
                location = lines[3]
            except:
                rating = 'null'
                title = lines[1]
                location = lines[2]

            try:
                salary = driver.find_element(by = By.CSS_SELECTOR, value = '.SalaryEstimate_medianEstimate__fOYN1').text
            except:
                salary = 'null'

            try:
                size = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(1) > div:nth-child(2)').text
            except:
                size = 'null'

            try:
                founded = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(2) > div:nth-child(2)').text
            except:
                founded = 'null'

            try:
                type = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(3) > div:nth-child(2)').text
            except:
                type = 'null'

            try:
                industry = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(4) > div:nth-child(2)').text
            except:
                industry = 'null'

            try:
                sector = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(5) > div:nth-child(2)').text
            except:
                sector = 'null'

            try:
                revenue = driver.find_element(by = By.CSS_SELECTOR, value = 'div.JobDetails_overviewItem__cAsry:nth-child(6) > div:nth-child(2)').text
            except:
                revenue = 'null'

            try:
                expand_desc = driver.find_element(by = By.CSS_SELECTOR, value = '.JobDetails_showMore___Le6L')
                expand_desc.click()
                time.sleep(1)
                job_desc = driver.find_element(by = By.XPATH, value = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div/div[1]/section/div[2]/div[1]').text
            except:
                job_desc = 'null' 

            try:
                xpath = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{i+1}]/div/div/div[1]/div[1]/div[4]/div[2]'
                skills = driver.find_element(by = By.XPATH, value = xpath).text
            except:
                skills = ''


            jobs.append({"Job Title": title,
                "Company Name": employer,
                "Salary Estimate": salary,
                "Rating": rating,
                "Job Description": job_desc,
                "Skills": skills,
                "Location": location,
                "Founded": founded,
                "Industry": industry,
                "Sector": sector,
                "Revenue": revenue,
                "Size": size,
                "Ownership Type": type})

            print(f'Success - {len(jobs)}')

        except:
            try:
                close = driver.find_element(by = By.CSS_SELECTOR, value = '.CloseButton')
                close.click()
            except:
                deets = 'NA'
                print('closing')

for url in urls:
    get_jobs(url)

driver.quit()

df = pd.DataFrame(jobs)

df.to_csv('jobs.csv', index=False)

