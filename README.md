# ROLEX PRICE ESTIMATOR
### CODESMITH - Classical Project - Cohort: Alpha 2
#### Authors: Paul Yim + Natalie Umanzor + Silvia Kocsis
#### December 2022


# Process:
1. Websraping Data from the webpage https://www.watchcollecting.com
Code is in `rolexVer009.py`
The path needs to be setup here: `service = Service('/usr/local/bin/chromedriver')`
The data are saved into file `dataAutoVer009.csv`

2. Websraping Data from the webpage https://www.ofx.com/en-us/forex-news/historical-exchange-rates/
Code is in `currencypaul002.py`
At the beginning the data are reading from file ```data\dataAutoVer009.csv```
At the end the updated data are exported into file ```dataWithCurrencyVer002.csv```

3. Code for data cleaning and preparing is in `cleaningRolexVer011WholeCode.py` At the beginning the data are reading from file `dataWithCurrencyVer002.csv`
At the end the updated data are exported into file `reformatedAndOneHotEncodedDataVer011.csv`

4. Model is created in the Jupiter Notebook: 
```Watches_Model.ipynb```
Model code is exported in ```watches_lgbm_initial_model.pkl```

5. Code for application is in files:
```server.py```

# To Do:
1. Make sure everything is able to be run

2. Finish flask server. Using the data received from the form, populate an array (should match the number of columns in the data set) to pass into the model to predict results. Once completed, test to see if the prediction is working and outputing data into the next page. (Tips are provided in the comments in the file)

3. Automate data retrieval such that webscraping will only scrape new entries to the website (i.e. new watches that were sold)

4. Automate model such that once enough new data has been retrieved the model will re fit to the best parameters in order to pickle into the flask server.

# Troubleshooting tips:
## Runnnig Selenium on MacBook

1. Download and install the latest Chrome and check your Chrome version
2. Download the Chrome WebDriver Zip File matching with your Chrome version and Apple Chip from ```https://chromedriver.storage.googleapis.com/index.html``` and extract the chromedriver
3. Copy the chromedriver and paste it to ```/usr/local/bin``` (If this folder doesn’t exist then create one)
4. Open a terminal inside the bin folder and run the following command so that MacOS can verify the app.
```
cd /usr/local/bin
xattr -d com.apple.quarantine chromedriver
```
5. Install Selenium: 
```
pip3 install selenium
```
6. When runnig code on MacOS, the ```py``` files for webscraping code should contain: 
```
service = Service('/usr/local/bin/chromedriver')
```



