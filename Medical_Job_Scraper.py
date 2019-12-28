# Job Web Scrapper
# import operator
#import csv
import json
import os
import smtplib
#import imghdr
from email.message import EmailMessage
from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen, Request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
#Javascript Webpages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# import requests
# import urllib.request
# from numpy import random
# import tensorflow as tf
# Engineering
# Kinneir Dufort
EMAIL_BIN = 'n'


class Company:
    registry = []

    def __init__(self, name, URL, Search):
        self.name = name
        self.URL = URL
        self.Search = Search
        self.registry.append(self)

def JavaGen_WebPage(Comp):
    chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("headless")
    driver = webdriver.Chrome(executable_path = r'C:/Users/lwsha/Downloads/chromedriver_win32/chromedriver.exe',options=chromeOptions)
    driver.get(Comp.URL)
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, Comp.Search)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    return(driver.page_source)

def WebScrape(Comp):
    Comp_Req = Request(url=Comp.URL, headers=headers)
    if Comp.name == 'Renishaw':
        Comp_html = JavaGen_WebPage(Comp)
    else:
        Comp_html = urlopen(Comp_Req).read()
    Comp_soup = BeautifulSoup(Comp_html, 'lxml')
    Comp_Jobs_Raw = Comp_soup.select(Comp.Search)
    job_list = []
    print('\n--' + Comp.name + '--')
    for i in Comp_Jobs_Raw:
        job = i.get_text().strip()
        job_list.append(job)
        print(job)
    return(job_list)


# Define Companies
# Engineering
KD = Company('Kinneir Dufort','https://www.kinneirdufort.com/join-us/', '.card__title')
OpenBio = Company('OpenBionics','https://openbionics.com/jobs/', 'h3.feature__heading.feature__heading--normal')
Crux = Company('Crux Product Design','http://www.cruxproductdesign.com/careers', 'h3')
#Renishaw = Company('Renishaw','https://renishaw.wd3.myworkdayjobs.com/Renishaw','.WI4Q.WKKY')
# Adventure
BAS = Company('British Antarctic Survey', 'https://www.bas.ac.uk/jobs/vacancies/', '.gsMedium.margin-top-none')
Stryker = Company('Stryker','https://careers.stryker.com/en-US/search?facetcountry=gb&facetcategory=engineering','a.primary-text-color.job-result-title')


# Get New Jobs
for Company in Company.registry:
    Company.Jobs = WebScrape(Company)
# KD.Jobs = WebScrape(KD)
# OpenBio.Jobs = WebScrape(OpenBio)
# Crux.Jobs = WebScrape(Crux)
# BAS.Jobs = WebScrape(BAS)
# Renishaw.Jobs = WebScrape(Renishaw)

# Convert Objects to Dictonary List
newJobDictList = []
for Company in Company.registry:
    Dict = vars(Company)
    del(Dict['Search'])
    newJobDictList.append(Dict)
# Save to File
# with open('Medical_Scrapper_Jobs.csv', 'w') as Jobs_File:
#     csv_writer = csv.writer(Jobs_File)
#     csv_writer.writerow([KD.name, ",".join(KD.Jobs)])
#     csv_writer.writerow([Crux.name, ",".join(Crux.Jobs)])

# Compare Jobs
with open('Grad_Jobs.json') as f:
    oldJobDictList = json.load(f)
# print(preJobDict)


def JobCompare(newJobDictList, oldJobDictList):
    # Get names of Companies
    newCompNameList = []
    oldCompNameList = []
    for Comp in newJobDictList:
        newCompNameList.append(Comp['name'])
    # print(newCompNameList)
    for Comp in oldJobDictList:
        oldCompNameList.append(Comp['name'])
    # print(oldCompNameList)

    # Compare File Companies and New Companies
    comSet = set(newCompNameList) & set(oldCompNameList)
    comLst = sorted(list(comSet))
    print('\n')
    print(comLst)
    # print(comLst)

    # Find index within Name lists for both new and old companies
    newJobIndex = []
    oldJobIndex = []
    for Job in comLst:
        newJobIndex.append(newCompNameList.index(Job))
        oldJobIndex.append(oldCompNameList.index(Job))

    # Compare Jobs with Common List of Companies
    print('\n')
    newJobInfo = []
    for i in range(len(comLst)):
        job_diff = set(newJobDictList[newJobIndex[i]]['Jobs']) - \
            set(oldJobDictList[oldJobIndex[i]]['Jobs'])
        if job_diff == set():
            print('{:<28}'.format(comLst[i] + ': ') + 'No New Jobs')
        else:
            print('{:<28}'.format(comLst[i] + ': ') + ', '.join(list(job_diff)))
            comp_name = newJobDictList[newJobIndex[i]]['name']
            comp_URL = newJobDictList[newJobIndex[i]]['URL']
            comp_new_jobs = list(job_diff)
            newJobInfo.append([comp_name,comp_URL,comp_new_jobs])       
    return(newJobInfo)

# Run Function
newJobInfo = JobCompare(newJobDictList, oldJobDictList)
print('\n')
if newJobInfo:
    numNewJob = len(newJobInfo)
    newJobSub = 'New Jobs @ '
    newJobBody = ''
    for i in range(numNewJob):
        if i == 0:
            newJobSub += newJobInfo[i][0]
        elif i == numNewJob-1:
            newJobSub += ' and ' + newJobInfo[i][0]
        else:
            newJobSub += ', ' + newJobInfo[i][0]
        #newjobbody
        newJobBody += newJobInfo[i][0] + '\n' + newJobInfo[i][1] + '\n' + ', '.join(newJobInfo[i][2])  + '\n\n'
    
    def YahWeh(msg_sub,msg_body): #Bruce Almighty Email
        EMAIL_ADDRESS = 'lwshaban@gmail.com'
        EMAIL_PASSWORD = 'ojtvdrhrmiscqfnk'

        msg = EmailMessage()
        msg['Subject'] = msg_sub
        msg['From'] = 'lwshaban@gmail.com'
        msg['To'] = 'lwshaban+python@gmail.com'

        msg.set_content(msg_body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        print('\nEmail Sent')
        return()
    if EMAIL_BIN == 'y':
        YahWeh(newJobSub,newJobBody)
else:
    print('\nNo New Jobs Found!')
#numNewJob = len(newJobInfo)
#print(newJobSub)
#print(newJobBody)

# Saving to Json
with open('Grad_Jobs.json', 'w') as f:
    json.dump(newJobDictList, f, indent=2)