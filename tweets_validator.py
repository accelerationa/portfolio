import json
import os
from line_validator import is_line_valid
from line_validator import parse_line
from utils import data_complete_rate
from constants import DATA_COMPLETE_RATE_BAR as PRESIDENCY_START_DATE
from utils import check_hour_data
import datetime 
from utils import timestamp_EDT_convert

def filter_tweets_with_company_name(company_name):
    filename = "trump.json"
    if not filename:
        print 'Error: file name not found'
        return

    with open(filename, 'r') as f:
        tweets = json.load(f)    

    #find tweets with company name
    tweets_with_company_name = list(filter(lambda x: company_name.lower() in x['text'].lower(), tweets))
    #map UTC time to timestamp
    map(date_str_to_timestamp, tweets)
    #sort tweets by tweeting date
    sorted(tweets_with_company_name, key = lambda d: d['created_at'])
    #filter out tweets before Trump presidency starts
    tweets_with_company_name = list(filter(lambda x: x['created_at'] >= 1484938095, tweets_with_company_name))
    #add EDT time field
    map(lambda d: d.update({'EDT time': timestamp_EDT_convert(d['created_at'])}), tweets_with_company_name)

    print json.dumps(tweets_with_company_name, indent=4, sort_keys=True)

def date_str_to_timestamp(d):
    '''
    Lambda function to help mapping UTC time to timestamp
    '''
    d['created_at'] = convert_date(d['created_at'])
    return d

def convert_date(date_str):
    '''
    date_str: date string in "Wed Aug 16 10:12:45 +0000 2017" format, where all time in UDT
    return: Timestamp
    '''
    date = date_str.replace('+0000 ','')
    assert(date != date_str)

    datetime_obj_naive = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
    timestamp = (datetime_obj_naive - datetime.datetime(1970, 1, 1)).total_seconds()
    return timestamp


if __name__ == "__main__":
    filter_tweets_with_company_name('Boeing')
    