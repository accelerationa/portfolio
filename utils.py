import datetime
import pytz


def data_complete_rate(data_list):
    dates = []
    previous_date = ""
    for data in data_list:
        if datetime.datetime.fromtimestamp(int(data['Time'])).strftime('%Y-%m-%d %H:%M:%S')[:10] != previous_date:
            previous_date = datetime.datetime.fromtimestamp(int(data['Time'])).strftime('%Y-%m-%d %H:%M:%S')[:10]
            dates.append(previous_date)
    
    return float(len(data_list)) / (len(dates) * 7)


def check_hour_data(date_str, data_list):
    '''
    This method is for checking the correctness of parsed data
    date_str: date string in "2018-01-29 15:00:00" format, all time are EDT time (New York)
    data_list: json formatted stock price data
    print: stock price at given date
    '''
    #print localized EDT time
    datetime_obj_naive = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    timestamp = (datetime_obj_naive - datetime.datetime(1970, 1, 1)).total_seconds()
    timestamp += 3600 * 4

    print date_str
    print filter(lambda n: n.get('Time') == timestamp, data_list)


def timestamp_EDT_convert(timestamp):
    '''
    Converts timestamp (10 digits) to EDT string: "2018-01-29 15:00:00 EDT" format
    '''
    timestamp = int(timestamp) + 3 * 3600
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S EDT')


def find_ratios(data_list, window_size, base_time):
    '''
    data_list: list of stock info, in json
    window_size: method return the ratio for the follow <window_size> hours
    base_time: the time Trump tweets, as a base time
    return as a json {'EDT time': <time>, 'ratio': <ratio>}
    '''
    count = 0
    started = False
    ratios = []
    last_close_price = 0
    for price in data_list:
        if count >= window_size:
            break
        if not started and price['Time'] >= base_time:
            started = True
        if started:
            count += 1

            ratios.append({
                'EDT Time': timestamp_EDT_convert(price['Time']),
                'Ratio': (float(price['Close']) - float(last_close_price)) / float(last_close_price),
                'Before hours change': (float(price['Open']) - float(last_close_price)) / float(last_close_price)
            })
        last_close_price = price['Close']

    return ratios