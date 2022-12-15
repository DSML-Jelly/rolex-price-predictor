# ROLEX PRICE ESTIMATOR
### CODESMITH - Classical Project - Cohort: Alpha 2
#### Authors: Paul Yim + Natalie Umanzor + Silvia Kocsis
#### December 2022

<br/>

# Process:
1. Websraping Data from the webpage https://www.watchcollecting.com
<br/>
Code is in ```rolexVer009.py```
The path needs to be setup here: ```service = Service('/usr/local/bin/chromedriver')```
The data are saved into file ```dataAutoVer009.csv```

2. Websraping Data from the webpage https://www.ofx.com/en-us/forex-news/historical-exchange-rates/
<br/>
Code is in ```currencypaul002.py```
<br/>
At the beginning the data are reading from file ```data\dataAutoVer009.csv```
At the end the updated data are exported into file ```dataWithCurrencyVer002.csv```

3. Code for data cleaning and preparing is in `cleaningRolexVer011WholeCode.py`

At the beginning the data are reading from file `dataWithCurrencyVer002.csv`
At the end the updated data are exported into file `reformatedAndOneHotEncodedDataVer011.csv`

4. Model is created in the Jupiter Notebook: 
<br/>
```Watches_Model.ipynb```
Model code is exported in ```watches_lgbm_initial_model.pkl```

5. Code for application is in files:
<br/>
```server.py```
<br/>

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



