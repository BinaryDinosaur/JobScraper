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
from webScrapePersonalInfo import emailAddress, emailPassword, webdriverPath
EMAIL_BIN = 'y'

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
    driver = webdriver.Chrome(executable_path = webdriverPath,options=chromeOptions)
    driver.get(Comp.URL)
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, Comp.Search)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    return(driver.page_source)

def WebScrape(Comp): #Webscraping Function based on CSS Classes
    Comp_Req = Request(url=Comp.URL, headers=headers)
    if Comp.name == 'Renishaw':
        Comp_html = JavaGen_WebPage(Comp)
    else:
        Comp_html = urlopen(Comp_Req).read()
    Comp_soup = BeautifulSoup(Comp_html, 'lxml')
    Comp_Jobs_Raw = Comp_soup.select(Comp.Search)
    #Remove Duplicates
    compJobsUnique=list(set(Comp_Jobs_Raw)) 
    job_list = []
    print('\n--' + Comp.name + '--')
    for i in compJobsUnique:
        if i.findAll('img'):
            img = i.find('img', alt=True)
            job = img['src']
        else:
            job = i.get_text().strip()
        job_list.append(job)
        print(job)
    return(job_list)

def JobCompare(newJobDictList): #Compare New and Old Jobs
    #Open List of Previous Job Searches
    with open('Grad_Jobs.json') as f:
        oldJobDictList = json.load(f)
    # Get names of Companies
    newCompNameList = []
    oldCompNameList = []
    for Comp in newJobDictList:
        newCompNameList.append(Comp['name']) #Get list of new companies
    # print(newCompNameList)
    for Comp in oldJobDictList:
        oldCompNameList.append(Comp['name']) #Get list of previous companies
    # print(oldCompNameList)

    # Compare File Companies and New Companies
    comSet = set(newCompNameList) & set(oldCompNameList) #Convert list to sets and add together to get all companies with no duplicates
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

def YahWeh(msg_sub,msg_body): #Bruce Almighty Email (Send Email)
    index = emailAddress.find('@') #Identify @ position in string
    emailToAddress = emailAddress[:index] + '+python' + emailAddress[index:] #Adds +python to my email address so I can easily filter the messages in my inbox

    msg = EmailMessage()
    msg['Subject'] = msg_sub #Email Subject
    msg['From'] = emailAddress #Email from
    msg['To'] = emailToAddress #Email to

    msg.set_content(msg_body) #Email Content

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(emailAddress, emailPassword)
        smtp.send_message(msg)
    
    print('\nEmail Sent')
    return()

## Define Company Shortlist
with open("Companies.json") as f:
    data=json.load(f)

for Comp in data:
    Company(Comp["name"],Comp["URL"],Comp["CSS"])
# Get New Jobs
for Company in Company.registry:
    Company.Jobs = WebScrape(Company)
# Convert Objects to Dictonary List
newJobDictList = []
for Company in Company.registry:
    Dict = vars(Company)
    del(Dict['Search'])
    newJobDictList.append(Dict)

# Compare Jobs
#newJobInfo = [] <- Use if Grad_Jobs.json is deleted
newJobInfo = JobCompare(newJobDictList)
print('\n')
#print(newJobInfo)
if newJobInfo:
    numNewJob = len(newJobInfo)
    newJobSub = 'New Jobs @ '
    newJobBody = ''
    for i in range(numNewJob):
        if i == 0: #Email Subject Structuring (if i==0 first company listing, elif i == numNewJob - 1 equals last company listing)
            newJobSub += newJobInfo[i][0]
        elif i == numNewJob-1:
            newJobSub += ' and ' + newJobInfo[i][0]
        else:
            newJobSub += ', ' + newJobInfo[i][0]
        #Email Body (Company Name, Website Link and all newly listed jobs)
        newJobBody += newJobInfo[i][0] + '\n' + newJobInfo[i][1] + '\n' + ', '.join(newJobInfo[i][2])  + '\n\n'
    YahWeh(newJobSub,newJobBody) #Send Email
else:
    print('\nNo New Jobs Found!')

# Saving to Json
with open('Grad_Jobs.json', 'w') as f:
    json.dump(newJobDictList, f, indent=2) #Save newly created company jobs dictionary to .json for future comparision.


######### Removed Companies List #######################
'''
    {
        "name":"Renishaw",
        "URL":"https://renishaw.wd3.myworkdayjobs.com/Renishaw",
        "CSS":"li.WBCR"
    },
'''