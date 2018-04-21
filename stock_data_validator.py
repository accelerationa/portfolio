import requests
import json
import os
from line_validator import is_line_valid
from line_validator import parse_line
from utils import data_complete_rate
from constants import DATA_COMPLETE_RATE_BAR as BAR
from utils import check_hour_data
import datetime 
from utils import find_ratios
from utils import timestamp_EDT_convert



def validate_stock_data(tweet_time):
    '''
    validates stock data from txt file to json file.
    data_list: the price lists, time is Timestamp
    Note: there may be data missing, BAR is set to 0.995, to ensure missing data is less than 0.5%
    '''

    url = 'https://www.google.com/finance/getprices?q=ADR&i=3600&p=1Y&f=d,c,h,l,o,v'
    response = requests.get(url).content

    data_str_list = response.split('\n')

    base_time = None
    data_list = []

    for data_line in data_str_list: 
        if is_line_valid(data_line):
            data, base_time = parse_line(data_line, base_time)
            data_list.append(data)
        
    print data_list
    print len(data_list)
    for data in data_list:
        print timestamp_EDT_convert(data['Time'])
    
    print json.dumps(data_list, indent=4, sort_keys=True)


    # Check correctness
    assert data_complete_rate(data_list) >= BAR
    check_hour_data("2018-01-29 15:00:00", data_list)
    check_hour_data("2018-02-28 11:00:00", data_list)
    check_hour_data("2018-03-12 10:00:00", data_list)

    ratios = find_ratios(data_list=data_list, window_size=10, base_time=tweet_time)
    print json.dumps(ratios, indent=4, sort_keys=True)

if __name__ == "__main__":
    validate_stock_data(1501840944.0)