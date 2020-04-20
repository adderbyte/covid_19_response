import pandas as pd
import twint
from datetime import datetime, timedelta
from time import sleep
import os


'''

This code was adapted from https://github.com/twintproject/twint/issues/604

Big thank you to the author https://github.com/jomorrcode

'''

def month_split(month):
    '''
    provides an increment on month 
    for looping over each month interval

    '''
    t =  int(month.split()[0][0]) # get the first digit
    q =  int(month.split()[0][1])  # get the secind
    #day = '01'
    if t==0 and q < 9: # check that first digit is less then 9 and t is zero
        q+=1 # increment q , this is the next month
        month = str(0) + str(q) # add zero to new int to give 2 gigit str 02 for examle

    else:
        month = str(int(month)+1) # otherwise turn integer to int and increment

    return month

def tweet_collector(query,s_month,e_month,duration,sleeptime=9000):

    '''
    e_month : end month for the first month, begining of next month

    s_start: first day of the month to be interrogated


    '''

    count = 0
    data_folder = "covid_tweets/"
    while count < duration:


        separator = '-'
        day= '01'
        start_str = year + separator+s_month + separator + day
        end_str =  year + separator+e_month + separator + day
        print('##################################################')
        print(start_str,end_str)
        print('##################################################')

        start_date = pd.to_datetime(start_str, format='%Y-%m-%d', errors='ignore')
        end_date = pd.to_datetime(end_str, format='%Y-%m-%d', errors='ignore')
        
        filename = f"{data_folder}covid_tweets_{start_str}_{end_str}.csv"
        resume_file = f"{data_folder}resume.txt"

        c = twint.Config()
        c.Hide_output = True
        c.Store_csv = True
        c.Output = filename
        c.Resume = resume_file
        c.Search = query
        c.Lang = 'en'
        print('Starting for the ... ', count+1,' loop' )
        while start_date < end_date:

            check = 0
            c.Since = datetime.strftime(start_date, format='%Y-%m-%d')
            c.Until = datetime.strftime(start_date + timedelta(days=1), format='%Y-%m-%d')
            
            while check < 1:
                try:
                    print("Running Search: Check ", start_date)
                    twint.run.Search(c)
                    check += 1

                except Exception as e:
                    # pause when twitter blocks further scraping
                    print(e, "Sleeping for 7 mins")
                    print("Check: ", check)
                    sleep(sleeptime)
            print('finished: ', c.Since, c.Until )
            # before iterating to the next day, remove the resume file
            os.remove(resume_file)

            # increment the start date by one day
            start_date = start_date + timedelta(days=1)
        

        s_month = month_split(s_month)
        e_month = month_split(e_month)
        
        count+=1


if __name__ == '__main__':
      query = 'coronavirus OR virus OR 2019-nCoV OR wuhan OR #WHO OR flu OR pneumonia OR Covid19 OR covid-19 OR vaccination OR Wuhan OR vaccines OR lockdown OR ICU'
      #query = 'coronavirus  OR flu OR 2019-nCoV OR wuhan OR  Covid19 OR covid-19 OR vaccines OR lockdown OR ICU'

      year = '2019'
      ## month interval of interest. This means we want from first month excluding 2nd month
      s_month = '08'  # ranges from 01 to 12
      e_month  = '09'  # ranges from 01 to 12
      # duration helps track the total month we want to compile
      duration = 1
      tweet_collector(query,s_month,e_month,duration)



