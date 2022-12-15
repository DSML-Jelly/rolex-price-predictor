from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd

############## READING DATA  ################
fileName='data\dataAutoVer009.csv'
df = pd.read_csv(fileName,header=0)

######################## CLEANING DATEs ##### 'listing__statTime' ##############
dates = list(df.listing__statTime.values)
# print(dates)
#  '26/04/21', '25/04/21', '23/04/21',

# checking incorect dates
# for date in dates:
#     if len(date)!=8 or date.count('/')!=2:
#         print(date)
# 5&nbsp;days
# 5&nbsp;days

DummyDate = '00/00/00'
reformatedDatesYYMMDD = []
reformatedDatesMMDDYY = []
reformatedDatesDDMMYY = []
for Date in dates:
    if len(Date)!=8 and Date.count('/')!=2:
        mmddyy = DummyDate
    else:
        ddmmyy = Date.split('/')
        yymmdd = ddmmyy[2] + '/' + ddmmyy[1] + '/' + ddmmyy[0]
    reformatedDatesYYMMDD.append(yymmdd)

# replace DummyDate with the median value
# median = np.median(reformatedDates) # can be used only for numbers
medianIndex=len(reformatedDatesYYMMDD)//2
median = sorted(reformatedDatesYYMMDD)[medianIndex]
# print('median=',median)
for i,Date in enumerate(reformatedDatesYYMMDD):
    if Date == DummyDate:
        reformatedDatesYYMMDD[i] = median
    yymmdd = reformatedDatesYYMMDD[i].split('/')
    mmddyy = yymmdd[1] + '/' + yymmdd[2] + '/' + yymmdd[0]
    ddmmyy = yymmdd[2] + '/' + yymmdd[1] + '/' + yymmdd[0]
    reformatedDatesMMDDYY.append(mmddyy)
    reformatedDatesDDMMYY.append(ddmmyy)

# print(dates[:10])
# print(reformatedDatesYYMMDD[:10])
# print(reformatedDatesMMDDYY[:10])

# df.listing__statTime = reformatedDatesMMDDYY
df.listing__statTime = reformatedDatesDDMMYY
# print(df.head(10))


##########


############################## PAUL vvvv
# for every unique currency
for currency in df.Currency.unique():
    # skip for USD
    if currency == 'USD':
        continue
    # grab every index of said currency
    index_GBP = df.index[df['Currency'] == currency].tolist()

    # def get_exchange(exchange):
    # service = Service('/users/paulj/chromedriver')

    # enabling headless mode
    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1920,1200")
    service = Service('/users/paulj/chromedriver')
    # service = Service('/usr/local/bin/chromedriver')   # Silvia
    #####################
    # driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)   # Paul
    driver.get("https://www.ofx.com/en-us/forex-news/historical-exchange-rates/")

    # get xpath of currency 1 and 2
    currency1 = driver.find_element(By.XPATH, '//*[@id="react-select-2-input"]') 
    currency2 = driver.find_element(By.XPATH, '//*[@id="react-select-3-input"]') 

    # Set input currency to CHF for exchange rate (can change to whatever is necessary depending on what currency it was sold in)
    currency1.send_keys(currency)
    currency1.send_keys(Keys.ENTER)

    # Set output currency to USD for exchange rate 
    currency2.send_keys('USD')
    currency2.send_keys(Keys.ENTER)

    # change radio button to get daily exchange rates
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="choice_frequency_daily"]')))
    frequency = driver.find_element(By.XPATH, '//*[@id="choice_frequency_daily"]')

    # scroll down such that click can work
    driver.execute_script("window.scrollBy(0,500)")
    time.sleep(0.4)
    action = ActionChains(driver)
    action.click(on_element = frequency)
    action.perform()

    # wait for react to load then set time period to past 3 years
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-select-4-input"]')))
    alltime = driver.find_element(By.XPATH, '//*[@id="react-select-4-input"]') 
    alltime.send_keys('3 Years')
    alltime.send_keys(Keys.ENTER)

    # click on retrieve to get data
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="post-113886"]/div/div[2]/div/section/section[1]/div/div[4]/div/a')))
    retrieve = driver.find_element(By.XPATH, '//*[@id="post-113886"]/div/div[2]/div/section/section[1]/div/div[4]/div/a')
    action = ActionChains(driver)
    action.click(on_element = retrieve)
    action.perform()

    # set time delay such that page can load
    time.sleep(10)

    # set todays date
    today = date.today()

    # for every index of currency
    for i in index_GBP:
        # convert to date
        sold_date = datetime.strptime(df.loc[i,['listing__statTime']].values[0], '%d/%m/%y').date()
        # grab starting date 
        three_years_back = today - relativedelta(years = 3)
        # get number of days passed since start
        initial_ind = sold_date - three_years_back 
        # change to integers
        initial_int = initial_ind.days
        print(initial_int)
        print(sold_date)
        if initial_int > 1075:
            initial_int = 1075
        # grab date of table with index position 
        str_soldDate = driver.find_element(By.XPATH, '//*[@id="post-113886"]/div/div[2]/div/section/section[2]/div[2]/div/table/tbody/tr['+ str(initial_int) +']/td[1]')
        date_sold = str_soldDate.get_attribute("innerHTML")
        # change table data to date object
        date_obj = datetime.strptime(date_sold, '%B %d,  %Y').date()
        # if table date matches dataframe date change sold price to USD
        if(date_obj == sold_date):
            exchange_rate = driver.find_element(By.XPATH, '//*[@id="post-113886"]/div/div[2]/div/section/section[2]/div[2]/div/table/tbody/tr['+ str(initial_int) +']/td[2]')
            df.loc[i,['listing__statPrice']] = int(df.loc[i,['listing__statPrice']]) * float(exchange_rate.text)
        # else change adjust the date index position for table to match and then change sold price to USD
        else:
            diff = date_obj - sold_date 
            initial_int = initial_int - diff.days
            exchange_rate = driver.find_element(By.XPATH, '//*[@id="post-113886"]/div/div[2]/div/section/section[2]/div[2]/div/table/tbody/tr['+ str(initial_int) +']/td[2]')
            df.loc[i,['listing__statPrice']] = int(df.loc[i,['listing__statPrice']]) * float(exchange_rate.text)

driver.quit()
# set all currency values to USD
df['Currency'] = 'USD'
df = df.drop(['Currency' , 'listing__statTime'], axis = 1)

#################### CREATING NEW CSV FILE ################################
print(df.columns)
print(df.head(10))

fileName='dataWithCurrencyVer002.csv'
df.to_csv(fileName)