#!/usr/bin/env python
# coding: utf-8

# ### Lockdown Dates Timeline

# In[1]:


import pycountry as pyctry
import re
import datefinder
import datetime
import pandas as pd
import requests
import urllib
from bs4 import BeautifulSoup
import csv
import calendar

# In[ ]:


# get list of month names
months = []
for i in range(1,12):
  months.append(calendar.month_name[i])


month = set(months)  

# In[2]:


# get the country names for querying wikipedia
country_names = []
for country in pyctry.countries:
        #country.name   #countries[country.name] = country.alpha_3
        country_names.append(country.name)


def lockdownExtractor(soup,countryname):
    collector = []
    # pattern to extract date of lockdown
    date_pattern = "\d{1,2}[/' '][a-zA-Z0-9]{3,}[/' ']\d{4}"
    # pattern 2 matches the case where the year was not reported 
    date_pattern2 = "\d{1,2}[/' '][a-zA-Z0-9]{3,}"
    # check month before day
    date_pattern3 = "[a-zA-Z0-9]{3,}\d{1,2}"
    add_year =  ' 2020'
    for elem in soup(text=re.compile(r' lockdown')):
        # get text element from element
        text = elem.parent.text 
        # Will return all the strings that matched the date_pattern 
        # date patterm reports day Month Year in full
        dates = re.findall(date_pattern, text)
        # if full date returns no match, then we have to dig dipper
        if not dates:
            ## check for digits and month as in pattern 2
            k = re.findall(date_pattern2, text) #re.findall(r'\d{1,2}\s+(\w+)', text)[0]
            for i in k:
                ## for all values matching pattern 2
                ## perform a split
                 temp = i.split()
                 
                 # check if split contains month name
                 #print(temp[0],temp[1])
                 if temp[1] not in month:
                    # if the lelement is not month continue
                    pass
                 else:
                    # if element it is a date
                    # retrive the date
                    dates = i + add_year
                    break
            # if date has not been retrieved up till now
            if not dates:
               # match the occurrence of Jan Feb to Dec and a digit 
               k =  re.findall(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+)',text)      # if no match found for k
               if not k:
                    # then date must be none
                    dates = None
               else:
                    # else set date to value of newly found match
                    dates =  k[0] 
        else:
            # if the full date is retrieved
            dates = dates[0]
       
        # if the date element is available
        if dates:
            #print(dates)
            # use date finder to return date data type and string generator
            matches = datefinder.find_dates(dates,source=True)
            # get the elements in the generator, 
            # this returns date as str, and date as datetime
            date = [i for i in   matches ]
            #print(date)
            
                
            # replace the str date element with '' and ':' with '', in text
            text = text.replace(date[0][1], '').replace(':','')
            # remove time stame from date in the datetime
            when = datetime.datetime.strptime(str(date[0][0]), '%Y-%m-%d  %H:%M:%S').date()
            # get the string date lement
            strs = date[0][1]
            collector.append((countryname,text,strs,when))
            #print(when,strs)
            #print('#######################')
        else:
            
            # if no date, append country name and 2 Nones
            collector.append((countryname,None,None,None))
    return collector

# In[ ]:





# In[4]:


query_term = 'lockdown'

# search link for data to be retrieved. country will be appended at the end
search_link = "2020_coronavirus_pandemic_in_" 
# part of the link to be queried
pre_url =  'https://en.wikipedia.org/wiki/' 
## header for the data to be stored
header = ['countryName','lockdownInfo','dateStr','date']


## specific url pattern. contains str that helps customize search per country
with open ('LockDownData/lockDownData.csv','wt') as csvfile:
    print('running ...')
    writer = csv.writer(csvfile, delimiter ="," )
    writer.writerow(header)
    
    for i in country_names:
        query_country = i # str('Chile')
        ## general url pattern to be queried
        search=  search_link +  query_country
        ### get the full link, pre url plus url key words
        link = pre_url + search
        ## get the data
        r = requests.get(link)
        # use beutiful soup for parsing
        soup = BeautifulSoup(r.text, "html.parser")
        # extract lockdown info
        temp = lockdownExtractor(soup,i)
        
        #write data to html
        [writer.writerow(i) for i in temp if i[1]!=None]
        
    
        
        


# In[ ]:





# In[363]:


#import pandas as pd


# In[366]:


#df = pd.DataFrame.from_records(n, columns =['Team', 'Age', 'Score']) 


# In[368]:


#df


# In[ ]:




