import pandas as pd
import re
import numpy as np
from collections import Counter
from functools import reduce

# fileName='dataAutoVer009.csv'
fileName='dataWithCurrencyVer002.csv'


df = pd.read_csv(fileName,header=0)
print(df.head(10))
# print(df.columns)
# print(set(df.CaseSize))
# print(Counter(df.CaseSize))
# print(df.shape)
'''
Index(['listing__statPrice', 'listing__statTime', 'product-subtitle', 'Model',
       'Box', 'Papers', 'Age', 'Movement', 'ConditionGrade', 'CaseSize',
       'Case', 'Dial', 'Bracelet', 'LOT', 'Location', 'Seller', 'Currency'],
      dtype='object')
'''

######################## DIALs ######### 'Dial' #######################
# Note: dialCounter does the same thing as df['Dial'].value_counts() 
dial = list(df.Dial.values)
dialCounter = Counter(dial)

# print(len(dialCounter))   # ->  141 items (now it's 143 items)
# print('K' in dialCounter,dialCounter['K'])  # False 0

keyWords = set()
for key in dialCounter:
    words = re.findall('[A-Z][^A-Z]*', key)
    for w in words:
        if 'with' in w:
            keyWords = keyWords.union(w.split('with'))
        else:
            keyWords = keyWords.union(words)

# print(keyWords) 
# print(len(keyWords))   # ->  107 items (now 108 items)
'''
{'', 'Sundustwith', 'Silverwith', "Honeycomb'", 'Hour', 'Pavé', "Cream'", 'K', 'D-blue', "Green'", 'Purple', 'Green', 'Grape', 'Z-blue', 'Pearlwith', 'Midnight', 'Flower', 'Red', 'Rhodium', 
'Palm', 'Baguette', 'Roman', 'Yellow', 'With', 'Stick', 'Indices', 'Blackand', 'Candy', 'Lapis', 'Salmon', 'Intense', 'Ice', 'Gilt', 'Arabic', 'Lotus', 'Pinkwithdiamonds', 'Greenwith', 
'Numeralwith', 'Sunburst', 'Numeral', 'Pearl', 'Applied', 'Blue', 'Turquoise', 'Pink', 'Motherof', 'Steel', 'Grey', 'Brown', 'Markers', 'Blue/', 'Gold', 'Slate', 'Motif', "Panda'", 
'Meteorite', 'Golden', 'Steel/', 'Sapphire', "Jubilee'", 'Slate)', 'Bright', 'Anthracite', 'Jubilee', 'Batonwith', 'Olive', 'Diamond', 'diamonds', 'Azzurro', 'Chocolate', 'Gradient', 'Ruby', 
'Racing', 'Ecru', 'Marks', 'Platinum', 'Lacquer', 'Pearl/', 'Coral', 'Polar', 'Rhodium(', 'Dial', 'White', 'Champagne', 'Set', 'Diamondand', 'Graduated', 'Sundust', 'Mint', "Motif'", 
'Champagnewith', 'Steeland', 'Black-', "Pink'", 'Blackwith', 'Rolex', "White'", 'Blac', 'Lazuli', 'Dial,', 'Baton', 'Motifwith', "Jubilee'with", 'Blue,', 'Numerals', 'Black', 'Silver'}
'''

typos = {}

cleanKeyWords = set()
for word in keyWords:
    word = word.replace('eee','ee')
    word = re.sub('[^a-zA-Z]','',word)
    if word[-3:] in {'and','And', 'set', 'Set', 'amp'}:
        word=word[:-3]
    if word[-4:] in {'with','With','gold','Dial','dial'}:
        word=word[:-4]
    if word[-2:] in {'of'}:
        word=word[:-2]
    if word[-1:] in {'/'}:
        word=word[:-1]
    if word[:-1] in keyWords:
        word='' # remove plural form of word
    if word in typos:
        word=typos[word]
    if 1<len(word):
        cleanKeyWords.add(word)

# print(len(cleanKeyWords))  # ->  73 items (still 73 descriptors)
# print(cleanKeyWords)

'''
{'Lapis', 'Applied', 'Sapphire', 'Ice', 'Champagne', 'Steel', 'Coral', 'Platinum', 'Sundust', 'Mint', 'Midnight', 'Turquoise', 'Baton', 'Green', 'Diamond', 'Salmon', 'Hour', 'Gold', 
'Purple', 'Meteorite', 'Jubilee', 'Ruby', 'Pav', 'Blac', 'Bright', 'Red', 'Lacquer', 'Silver', 'Dblue', 'Lazuli', 'Gilt', 'Slate', 'Candy', 'Indices', 'Anthracite', 'Numeral', 'Stick', 
'Racing', 'Zblue', 'diamonds', 'Panda', 'White', 'Palm', 'Pink', 'Ecru', 'Cream', 'Motif', 'Rhodium', 'Baguette', 'Brown', 'Chocolate', 'Gradient', 'Azzurro', 'Golden', 'Grape', 'Grey', 
'Graduated', 'Yellow', 'Intense', 'Marks', 'Honeycomb', 'Sunburst', 'Markers', 'Roman', 'Lotus', 'Flower', 'Rolex', 'Mother', 'Pearl', 'Polar', 'Arabic', 'Blue', 'Olive'}
'''

# colors = {'Golden', 'Blac', 'Ecru', 'Brown', 'Honeycomb', 'Yellow', 'White', 'Mint', 'Cream',  'Dblue', 'Pink', 'Purple', 'Green', 'Turquoise', 'Red', 'Zblue', 'Blue', 'Champagne', 
#           'Grey', 'Anthracite', 'Azzurro', 'Olive', 'Chocolate', 'Salmon'}
# noColors = {'Rhodium', 'Lapis', 'Pearl', 'Steel', 'Stick', 'Baguette', 'Gilt', 'Applied', 'Midnight', 'Candy', 'Lacquer', 'Platinum', 'Polar', 'Intense', 'Slate', 'Panda', 'Lazuli', 
#             'Mother', 'Flower', 'Rolex', 'Silver', 'Hour', 'Racing', 'Jubilee', 'diamonds', 'Motif', 'Bright', 'Indices', 'Pav', 'Gold', 'Sunburst', 'Grape', 'Ruby', 'Graduated', 
#             'Sundust', 'Roman', 'Diamond', 'Baton', 'Arabic', 'Sapphire', 'Meteorite', 'Markers', 'Palm',  'Numeral', 'Ice', 'Gradient', 'Lotus', 'Marks', 'Coral'}
# print('Colors:',len(colors))
# print('noColors:',len(noColors))

newDialCounter = {}
for word in cleanKeyWords:
        newDialCounter[word]=0
for i in range(len(df)):
    actual = df.loc[i,'Dial']
    for word in cleanKeyWords:
        if word in actual:
            newDialCounter[word]+=1
# print(newDialCounter)

groups = { 'allDiamond': ['Pav'],
           'preciousStone': ['Lazuli', 'Meteorite', 'Lapis', 'Mother', 'Pearl'],
           'someDiamonds': ['Baguette', 'Jubilee', 'diamonds', 'Applied', 'Diamond', 'Indices'],
        #    'noDiamonds': ['Azzurro', 'Turquoise','Silver', 'Bright', 'Yellow', 'Arabic', 'Lotus', 'Zblue', 'Polar', 'Purple','Baton', 'Markers', 'Sapphire', 'Blue', 'Ruby', 'Champagne', 
        #    'Panda', 'Ice', 'Lacquer','Blac','Brown', 'Midnight', 'Anthracite', 'Sundust', 'Ecru', 'Motif', 'Cream', 'White', 'Marks', 'Roman', 'Flower', 'Palm','Slate','Graduated', 'Dblue', 
        #    'Salmon', 'Hour', 'Chocolate','Coral','Golden', 'Pink', 'Rhodium','Green', 'Grape', 'Gilt', 'Sunburst', 'Platinum', 'Intense', 'Steel', 'Grey', 'Stick', 'Gold', 'Gradient', 
        #    'Rolex', 'Racing', 'Olive', 'Numeral', 'Red', 'Candy', 'Mint', 'Honeycomb'],    
         }

# Manual One Hot Encoding with groups
whichGroup = {}
for group in groups:
    for word in groups[group]:
        whichGroup[word]=group
# print(whichGroup)

# Same as len(df) 
n = df.shape[0]

for key in groups.keys():
    # This creates new columns in df that are all 0s 
    df[key] = [0]*n
# This creates a set of all of the values that were in their groups dictionary
groupsFlatten = set(reduce(lambda a,b:a+b, groups.values()))
for i in range(len(df)):
    # This is the value (string) that's in df['Dial']
    actual = df.loc[i,'Dial']
    for word in groupsFlatten:
        if word in actual:
            # Add 1 to the corresponding column (allDiamond, preciousStone, or someDiamonds)
            df.loc[i,whichGroup[word]] = 1
df = df.drop('Dial', axis=1)
# print(df.head()
# print(df[['Dial','allDiamond','preciousStone','someDiamonds']].head(30))
print()
print('DIAL One-Hot-Encoding Finished.')


######################## BRACELETs ######### 'Bracelet' #######################

# Note: braceletCounter does the same thing as df.Bracelet.value_counts()
bracelet = list(df.Bracelet.values)
braceletCounter = Counter(bracelet)

# print(len(braceletCounter))   # ->  83 items
# print('K' in braceletCounter,braceletCounter['K'])

keyWords = set()
for key in braceletCounter:
    words = re.findall('[A-Z][^A-Z]*', key)
    keyWords = keyWords.union(words)
# print(keyWords)
'''
{'Steeland', 'Presdient', 'Jubileee', 'Rose', 'Alligator', 'Pearlmaster', 'Oysyerflex', 'Oysterflex', 'Platinum', 'Steel&amp;', 'Crocodile', 'Goldand', 'Pink', 'Everose', 
'Stainless', 'Steel/', 'Gold,', 'Oyster', 'Brown', 'Fabric', 'Black', 'Steel&amp;18', 'K', 'Braclelet', 'Steel,', 'Yellow', 'And', 'Steel', 'Jubilee', 'Leather', 'Rubber', 
'White', 'President', 'Bracelet', 'Strap', 'Gold', 'Flex'}
'''

typos = {'Presdient':'President','Braclelet':'Bracelet','Oysyerflex':'Oysterflex'}

cleanKeyWords = set()
for word in keyWords:
    word = word.replace('eee','ee')
    word = re.sub('[^a-zA-Z]','',word)
    if word[-3:] in {'and','And', 'set', 'Set', 'amp'}:
        word=word[:-3]
        # print(word)
    if word[-4:] in {'with','gold'}:
        word=word[:-4]
    if word[-1:] in {'/'}:
        word=word[:-1]
    if word[:-1] in keyWords:
        word='' # remove plural form of word
    if word in typos:
        word=typos[word]
    if 1<len(word):
        cleanKeyWords.add(word)

# print(cleanKeyWords)
# print(len(cleanKeyWords))  # ->  24 items (still 24 items)
'''
{'Bracelet', 'Fabric', 'Rubber', 'Oyster', 'Brown', 'Steel', 'President', 'Pearlmaster', 'Everose', 'Alligator', 'Pink', 'Platinum', 'Oysterflex', 'Rose', 'Black', 'White', 
'Crocodile', 'Gold', 'Strap', 'Stainless', 'Yellow', 'Flex', 'Leather', 'Jubilee'}
'''

groups = {'braceletRubber' : ['Rubber', 'Black', 'Strap'],
         'braceletLeather' : ['Leather', 'Brown', 'Alligator', 'Crocodile'],
         'braceletFabric'  : ['Fabric'],
	     'braceletMetal'   : ['Yellow', 'Pearlmaster', 'Platinum', 'Bracelet', 'Pink', 'White', 'Steel', 'Oysterflex', 'Gold',
                              'Stainless', 'Everose', 'Oyster', 'Flex', 'President', 'Jubilee', 'Rose']
         }

# Manual One Hot Encoding with groups
whichGroup = {}
for group in groups:
    for word in groups[group]:
        whichGroup[word]=group
# print(whichGroup)

n = df.shape[0]

for key in groups.keys():
    df[key] = [0]*n

for i in range(len(df)):
    actual = df.loc[i,'Bracelet']
    for word in cleanKeyWords:
        if word in actual:
            df.loc[i,whichGroup[word]] = 1
df = df.drop('Bracelet', axis=1)
# print(df.head(10))

print('BRACELET One-Hot-Encoding Finished.')


######################## CASEs ######### 'Case' #######################
cases = list(df.Case.values)
# print(cases[:30])
casesCounter = Counter(cases)
# print(casesCounter)
'''
Counter({'StainlessSteel': 476, 'YellowGold': 71, 'StainlessSteelandYellowGold': 66, 'WhiteGold': 52, 
'RoseGold': 45, 'StainlessSteelandWhiteGold': 25, 'StainlessSteelandRoseGold': 23, 'SteelandYellowGold': 11, 
'Platinum': 9, 'StainlessSteelandPlatinum': 5, 'Steel': 4, 'SteelandRoseGold': 4, 'EveroseGold': 3, 'WhiteGoldandPlatinum': 3, 
'StainlessSteel&amp;RoseGold': 3, 'SteelandGold': 3, 'Gold': 3, 'StainlessSteel&amp;YellowGold': 3, 'StainlessSteel&amp;WhiteGold': 3, 
'StainlessSteelAndWhiteGold': 2, 'StainlessSteelAndYellowGold': 2, 'Steel&amp;YellowGold': 2, '18KYellowGold': 2, 'OysterSteel': 2, 
'Steel&amp;Platinum': 2, 'StainlessSteel/Gold': 2, 'Steel/YellowGold': 1, 'Steel/YellowGold/Diamond': 1, 'Steel&amp;18KYellowGold': 1, 
'WhiteGoldwithDiamondSet': 1, 'StainlessSteeel': 1, 'YellowGoldwithDiamonds': 1, 'SteelandWhiteGold': 1, 'PlatinumwithDiamond': 1, 
'YellowGoldwithDiamond': 1, 'StainlessandYellowGold': 1, 'Yellowgold': 1, 'YellowGoldOyster': 1, 'RoseGoldandStainlessSteel': 1, 
'StainlessSteel&amp;Gold': 1, 'StainlessSteel/Everose': 1, 'StainlessSteelandGold': 1, 'Steel&amp;Gold': 1, '41mm': 1, 'SteelandPlatinum': 1, 
'Steel/Gold': 1})
'''
# print(len(casesCounter))   # ->  46 items

keyWords = set()
for key in casesCounter:
    words = re.findall('[A-Z][^A-Z]*', key)
    keyWords = keyWords.union(words)
# print(keyWords)

cleanKeyWords = set()
for word in keyWords:
    word = word.replace('eee','ee')
    word = re.sub('[^a-zA-Z]','',word)
    if word[-3:] in {'and','And', 'set', 'Set', 'amp'}:
        word=word[:-3]
    if word[-4:] in {'with','gold'}:
        word=word[:-4]
    if word[-1:] in {'/'}:
        word=word[:-1]
    if word[:-1] in keyWords:
        word='' # remove plural form of word
    if 1<len(word):
        cleanKeyWords.add(word)

# print(cleanKeyWords)
# {'White', 'Yellow', 'Stainless', 'Rose', 'Oyster', 'Diamond', 'Everose', 'Steel', 'Gold', 'Platinum', 'Steelamp'}


n = df.shape[0]
# print(df.shape,n)
for word in cleanKeyWords:
    df['case'+word] = [0]*n
# print(df.shape)

for i in range(len(df)):
    actualCase = df.loc[i,'Case']
    for word in cleanKeyWords:
        if word in actualCase:
            df.loc[i,'case'+word] = 1

df = df.drop('Case', axis=1)
# print(df.head(10))

print('CASE One-Hot-Encoding Finished.')

'''
######################## MOVEMENTs ######### 'Movement' #######################
movement = list(df.Movement.values)
print(movement[:30])
print(set(movement))
# {'quartz', 'automatic', 'manual'}
print(Counter(movement))
# Counter({'automatic': 831, 'manual': 11, 'quartz': 4})
'''

######################## CASE SIZEs ######### 'CaseSize' #######################
caseSize = list(df.CaseSize.values)
# print(caseSize[:30])

reformatedCaseSize = []
for case in caseSize:
    num = re.findall('\d+',case) + ['0']
    reformatedCaseSize.append(int(num[0]))

# print(reformatedCaseSize.count('0'))  # 2 zero items
median = np.median(reformatedCaseSize) 
for i,case in enumerate(reformatedCaseSize):
    if not case:
        reformatedCaseSize[i]=median

# print(reformatedCaseSize.count(0))  # 0 zero items
# print(reformatedCaseSize[:30])
# print('reformatedCaseSize',set(reformatedCaseSize))
df.CaseSize = reformatedCaseSize
# print(df.head(10))
# Case Size Categories: 32-34, 34-36, 36-38, 38-40, 40-42, 44+
thresholds = [32,34,36,38,40,42,44]
categoryCaseSizes = reformatedCaseSize

for t in thresholds:
    df['CaseSize'+str(t)] = [0]*n
for i in range(len(df)):
    actual = df.loc[i,'CaseSize']
    for t in thresholds:
        if actual<=t:
            df.loc[i,'CaseSize'+str(t)] = 1
            break
df = df.drop('CaseSize', axis=1)

print('CASE SIZE Reformating Finished.')

'''
######################## CLEANING DATEs ##### 'listing__statTime' ##############
dates = list(df.listing__statTime.values)
# print(dates)
#  '26/04/21', '25/04/21', '23/04/21',

# checking incorect dates
for date in dates:
    if len(date)!=8 or date.count('/')!=2:
        print(date)
# 5&nbsp;days
# 5&nbsp;days

DummyDate = '00/00/00'
reformatedDatesYYMMDD = []
reformatedDatesMMDDYY = []
for date in dates:
    if len(date)!=8 and date.count('/')!=2:
        mmddyy = DummyDate
    else:
        ddmmyy = date.split('/')
        yymmdd = ddmmyy[2] + '/' + ddmmyy[1] + '/' + ddmmyy[0]
    reformatedDatesYYMMDD.append(yymmdd)

# replace DummyDate with the median value
# median = np.median(reformatedDates) # can be used only for numbers
medianIndex=len(reformatedDatesYYMMDD)//2
median = sorted(reformatedDatesYYMMDD)[medianIndex]
# print('median=',median)
for i,date in enumerate(reformatedDatesYYMMDD):
    if date == DummyDate:
        reformatedDatesYYMMDD[i] = median
    yymmdd = reformatedDatesYYMMDD[i].split('/')
    mmddyy = yymmdd[1] + '/' + yymmdd[2] + '/' + yymmdd[0]
    reformatedDatesMMDDYY.append(mmddyy)

print(dates[:10])
print(reformatedDatesYYMMDD[:10])
print(reformatedDatesMMDDYY[:10])

df.listing__statTime = reformatedDatesMMDDYY
print(df.head(10))

'''
#################### CODE FROM PAUL ################################
groups = {
    'daydate': ['day'],
    'datejust': ['datejust', 'date'],
    'oysterperpetual': ['perpetual', 'oyster'],
    'ladydatejust': ['lady'],
    'cellini': ['cellini'],
    'airking': ['air', 'king'],
    'gmtmaster': ['gmt'],
    'yachtmaster': ['yachtmaster', 'yacht'],
    'submariner': ['submariner'],
    'cosmographdaytona': ['daytona', 'cosmograph'],
    'seadweller': ['deepsea', 'sea'],
    'skydweller': ['sky'],
    'explorer': ['explorer'],
    'milgauss': ['milgauss'],
    'other': ['chronograph', 'precision', 'royal', 'oysterquartz', 'pearlmaster', 'prince']
    }
years = ['2018-2022', '2013-2017', '2008-2012', '2003-2007', 'Vintage']

df = df.replace(np.nan, 'other', regex = True)

key_val_title = list(groups.keys())
key_val_title
n = df.shape[0]

# print(df.shape,n)

for movement in df['Movement'].unique():
    df['Movement'+ movement] = [0]*n
for Paper in df['Papers'].unique():
    df['Papers'+Paper] = [0]*n
for Box in df['Box'].unique():
    df['Box'+Box] = [0]*n
for condition in df['ConditionGrade'].unique():
    # if condition == 0:
    #     df['Condition' + 'other'] = [0]*n
    # else:
    df['Condition'+condition] = [0]*n
    
for five_years in years:
    df['Manufacture'+five_years] = [0]*n
for title in key_val_title:
    df['Product'+title] = [0]*n
# print(df.shape)

for i in range(len(df)):
    actualProduct = df.loc[i,'Age']
    # change age to ranges
    if actualProduct == '41mm':
        actualProduct = '2022'
    actualProduct = int(actualProduct[:4])
    if actualProduct >= 2018:
        df.loc[i,'Manufacture'+years[0]] = 1
    elif actualProduct >= 2013:
        df.loc[i,'Manufacture'+years[1]] = 1
    elif actualProduct >= 2008:
        df.loc[i,'Manufacture'+years[2]] = 1
    elif actualProduct >= 2003:
        df.loc[i,'Manufacture'+years[3]] = 1
    else:
        df.loc[i,'Manufacture'+years[4]] = 1
    
    # change product titles to keywords
    actualTitle = df.loc[i,'product-subtitle']
    actualTitle = re.sub('[^a-zA-Z]','', actualTitle).lower()
    for key, val_list in groups.items():
        for val in val_list:
            if val in actualTitle:
                df.loc[i,'Product' + key] = 1

    # chnage condition to one hot encode
    actualCondition = df.loc[i,'ConditionGrade']
    # if actualCondition == 0:
    #     df.loc[i,'Condition' + 'other'] = 1
    # else:
    df.loc[i,'Condition' + actualCondition] = 1

    # chnage condition to one hot encode
    actualBox = df.loc[i,'Box']
    df.loc[i,'Box' + actualBox] = 1

    # chnage condition to one hot encode
    actualPapers = df.loc[i,'Papers']
    df.loc[i,'Papers' + actualPapers] = 1

    # chnage condition to one hot encode
    actualMovement = df.loc[i,'Movement']
    df.loc[i,'Movement' + actualMovement] = 1


df = df.drop(['Movement' , 'Age', 'ConditionGrade', 'Papers', 'Box', 'product-subtitle', 'Model', 'LOT', 'Location', 'Seller'], axis = 1)


#################### CREATING NEW CSV FILE ################################
print(df.columns)
print(df.head(10))

fileName='reformatedAndOneHotEncodedDataVer011.csv'
df.to_csv(fileName)
