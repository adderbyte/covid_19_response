import pycountry as pyctry
import re
import datefinder
import datetime
import pandas as pd
import requests
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import bs4
import os
import numpy as np

################
# current working directory
cw = os.getcwd()
###############


###################################
# folder for saving model
if not os.path.exists('LockDownData'):
    print('Preparing folder for saving model ...')
    os.makedirs('LockDownData')

# get current directory
savepath = cw + '/LockDownData/'
#######################################


####################################################################################
# url
url = 'https://en.wikipedia.org/wiki/Curfews_and_lockdowns_related_to_the_2019%E2%80%9320_coronavirus_pandemic'
# resource request
res = requests.get(url).text
#load in beutiful soup
soup = bs4.BeautifulSoup(res, "lxml")
##########################################################################################



########################################################################################333
# table of interest is of class wiki table sortable
My_table=soup.find('table', class_='wikitable sortable mw-collapsible')
# All tables are loaded here 
alltables = soup.find_all('table', {"class":"wikitable"})



#### Lock daown info for all countries
rows = My_table.findAll(lambda tag: tag.name=='tr')


# for storing all data 
header =None
# keys for dictionaries
keys = []
# for storing immediate values in dictionaries
check = None


for i in rows:
    
    if rows.index(i) == 0 : 
        pass
    elif rows.index(i) == 1:
        t = [th.getText().strip() for th in i.find_all('th') if th.getText().strip() != '']
        header = {k:[] for k in t}
        
        keys = t
        print(keys)
    else:
        #k = [td.getText().strip() for td in i.find_all('td') if td.getText().strip() != ''  ] 
        #k= [td.getText().strip() for td in i.find_all('td')]
        tableData =  i.find_all('td')
        length  =  len(tableData)
        #s= i
        #print(k)
        #y.append(k)
        #lambda x = 
        count=0
        temp = []
        if  length== len(keys):
            #print(length)
            for i in range(0,length):
                header[keys[i]].append(tableData[i].getText().strip())
                temp.append(tableData[i].getText().strip())
        #['Countries and territories', 'Place', 'Start date', 'End date', 'Level']
        
        else:
            check = {k:None for k in keys}
            
            for i in range(0,length):
                if i == 0:
                    #temp.append(tableData[i].getText().strip())
                    test = '2020 coronavirus pandemic'
                    try:
                        text = tableData[i].find('a').get('title')
                        if test in text:
                            #header[keys[i]].append(tableData[i].getText().strip())
                            check[keys[i]] = tableData[i].getText().strip()
                        else:
                            #header[keys[1]].append(tableData[i].getText().strip())
                            #header[keys[0]].append(header[keys[0]][-1])
                            check[keys[0]] = header[keys[0]][-1]
                            check[keys[1]] = tableData[i].getText().strip()#header[keys[1]][-1]
                            if length == 1:
                                check[keys[2]] = header[keys[2]][-1]
                                check[keys[3]] = header[keys[3]][-1]
                                check[keys[4]] = header[keys[4]][-1]
                                #print(tableData[i].getText().strip())
                            #print(check)

                            
                    except:
                        temp= []
                            
                else:
                    
                    #l = tableData[i].getText().strip()
                    temp.append(tableData[i].getText().strip())
                    # print([i for i in k])
            
            count = 0;
            
            if length != 1:
                for j in temp:

                    r=[ i for i in datefinder.find_dates(j,source=True)  ]

                    if r :
                        if count ==0:
                            #header[keys[2]].append(r[0][1]) 
                            check[keys[2]]=r[0][1] 
                            count +=1
                        else:
                            #header[keys[3]].append(r[0][1])
                            check[keys[3]]=r[0][1]
                    else:
                        if count ==0 and check[keys[1]]==None:
                               #header[keys[1]].append(j) 
                               check[keys[1]]= j
                               count +=1
                        else:
                               #header[keys[4]].append(j)
                               check[keys[4]]=j
                    
            for k,v in check.items():
                #print(v)
                
                #if not v:
                header[k].append(v)    #pr


##################################################################################################################



############################################################################
# create datafame from, data 
allCountriesLockdown=pd.DataFrame(header, columns= keys)
# file name 
file_name =  'allCountriesLockdown.csv'
# save the data
allCountriesLockdown.to_csv(savepath + file_name,index=None)
############################################################################




# china specific data 
metadata_covidLockdownChina = [] # data metadata
table_contents = []   # store your table here
rows = alltables[3].findAll(lambda tag: tag.name=='tr')
title=None
column_names = None
for tr in rows:
    if rows.index(tr) == 0 : 
        title = [th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '']
        print('Table title: ', title)
    if rows.index(tr) == 1 : 
        column_names =([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != ''  ]   
        print('Table column names: ',column_names)  
    else : 
        row_cells = ([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != ''  ] 
    if len(row_cells) > 1 : 
        table_contents += [ row_cells ]






metadata_covidLockdownChina.append([  ('title: ', title)   , ('Quarantine Total' ,column_names[5:] ,  table_contents[-1]    ) ]    )


############################################################################
# create datafame from, data 
covidLockdownChina =   pd.DataFrame.from_records(table_contents[:-1], columns=column_names) 
# file name 
file_name =  'covidLockdownChina.csv'
metadataName = 'metadata_covidLockdownChina'
# save the data
covidLockdownChina.to_csv(savepath + file_name,index=None )

# save metadata
np.save(savepath+metadataName,metadata_covidLockdownChina)


############################################################################












