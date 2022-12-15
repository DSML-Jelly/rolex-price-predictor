from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from random import randint
import time
from time import sleep
import json
import math
from selenium.webdriver.chrome.service import Service
import pandas as pd
import csv

# https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html

# enabling headless mode
options = Options()
options.headless = True
# options.add_argument("--window-size=1920,1200")

# service = Service('/users/paulj/chromedriver')
service = Service('/usr/local/bin/chromedriver')
#####################
driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
# driver = webdriver.Chrome(service=service)


driver.get("https://www.watchcollecting.com")

# print(driver.page_source)
# htmlPageSource = driver.page_source
# print(len(htmlPageSource))
# print(htmlPageSource[:40])

# https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=1
# https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=2
# https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=3


mainURL = "https://www.watchcollecting.com"

# website="https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=1"
# driver.get(website)

# listOfAuctions = []
# for auction in driver.find_elements(By.CLASS_NAME, 'auction'):
#     listOfAuctions.append(auction.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

# while not listOfAuctions:
#     time.sleep(1)

def processAuction(auction):
    # driver.get(listOfAuctions[0])
    driver.get(auction)
    dataDict = {}
    for className in ['listing__statPrice', 
                    'listing__statTime', 
                    'product-subtitle', 
                    'reference-number']:

        value = driver.find_element(By.CLASS_NAME, className).get_attribute('innerHTML')
        value = re.sub('\s+', '', value).strip()
        dataDict[className] = value

    # Process reference-number
    key,value = dataDict['reference-number'].split(':')
    key = key.strip()
    value = value.strip()
    dataDict[key] = value
    del dataDict['reference-number']

    # Process listing__statPrice
    value = dataDict['listing__statPrice']
    value = re.findall('\d',value)
    dataDict['listing__statPrice'] = int(''.join(value))


    for element in driver.find_elements(By.CLASS_NAME, 'column'):
        for detail in driver.find_elements(By.TAG_NAME, 'li'):
            attribute = detail.get_attribute('innerHTML')
            if attribute[:27] == '<span class="column-title">':
                parsedSpan = attribute[27:].split('</span>')
                # <span class="column-title">Box:</span>Yes 
                key = parsedSpan[0][:-1]
                value = parsedSpan[-1].strip()
                # value is until the next tag starting, if exist
                value = value.split('<')[0]
                key = re.sub('\s+', '', key).strip()
                value = re.sub('\s+', '', value).strip()
                dataDict[key] = value

    # print(dataDict)
    return dataDict


################################

def getListOfDictionaries(website):
    listOfDictionaries = []
    driver.get(website)
    listOfAuctions = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'auction')))
    for auction in driver.find_elements(By.CLASS_NAME, 'auction'):
       listOfAuctions.append(auction.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))

    for auction in listOfAuctions:
        listOfDictionaries.append(processAuction(auction))

    return listOfDictionaries

# data = getListOfDictionaries()
# print(data)

################################
# Number of pages
website="https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=1"
driver.get(website)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div[2]/div/div[1]/div/a[4]/span')))
searchNumber = driver.find_element(By.XPATH, '/html/body/main/div[2]/div/div[2]/div/div[1]/div/a[4]/span').get_attribute('innerHTML')
# instead of 24 you can use length of list of items 
num_pages = math.ceil(int(searchNumber) / 24)
print('searchNumber is', searchNumber)
print('num_pages is',num_pages)

################################
# We need to wait until a certain condition become true = the scrapping the previous page is done
# https://stackoverflow.com/questions/2785821/is-there-an-easy-way-in-python-to-wait-until-certain-condition-is-true
# def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
#   mustend = time.time() + timeout
#   while time.time() < mustend:
#     if somepredicate(*args, **kwargs): return True
#     time.sleep(period)
#   return False
################################

# website="https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page=1"
website="https://www.watchcollecting.com/?refinementList%5Bstage%5D%5B0%5D=sold&refinementList%5BvehicleMake%5D%5B0%5D=Rolex&page="
data = []
keysCSV = []
dataCSV = []

# sleep(randint(2,10))

# for i in range(1,num_pages+1):
# for i in range(1,5):
# for i in range(5,10):
# for i in range(10,15):
# for i in range(15,20):
# for i in range(20,25):
# for i in range(25,30):
# for i in range(30,num_pages+1):
for i in range(1,num_pages+1):
# for i in range(1,2)
    # lenDataBefore=len(data)
    # sleep(randint(2,10))
    # sleep(randint(20,50))
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "waitCreate")))

    scrapListOfDict = getListOfDictionaries(website + str(i))
    data.append(scrapListOfDict)

    for rowAsDict in scrapListOfDict:
        # print(rowAsDict)
        rowCSV = []
        if keysCSV:
            for key,val in rowAsDict.items():
                rowCSV.append(val)
        else:
            for key,val in rowAsDict.items():
                keysCSV.append(key)
                rowCSV.append(val)
        if not dataCSV:
            dataCSV.append(keysCSV)
        dataCSV.append(rowCSV)
print(dataCSV[:100])



    # WebDriverWait(driver, 10).until(lenDataBefore<len(data))  # TypeError: 'bool' object is not callable
    # while lenDataBefore==len(data):
    #     sleep(randint(2,10))

# print(data)


driver.quit()
################################
fileName='dataAutoVer009.json'

with open(fileName, 'w') as file:
    json.dump(data, file)

################################
fileName='dataAutoVer009.csv'

# with open(fileName, 'w') as file:
#     json.dump(dataCSV, file)

with open(fileName, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # # write the header
    # writer.writerow(header)

    # write multiple rows
    writer.writerows(dataCSV)

