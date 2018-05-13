from pandas import *
from numpy import *
from operator import *
import statsmodels.formula.api as sm
import pprint
import operator
from pandas_datareader import data as pdr
import datetime
import urllib
import re
import json
import datetime
import glob, os


DATA_FOLDER = "data"



Tickers=read_table('Ticker.txt')
Ticker=transpose(array(Tickers)).tolist()
Ticker=Ticker[0]


def main():
    ls_key = 'Close'        
    start = datetime.datetime(2017,12,1)     
    end = datetime.datetime.now()
    f =pdr.DataReader('ITB','morningstar',start,end)       
    data={'ITB': array(DataFrame(f[ls_key])).tolist()}
    dataFrame=DataFrame(data)
    Stock_n=Ticker[:]

    for i in range(0,len(Stock_n)):
        try:
            f =pdr.DataReader(Stock_n[i],'morningstar',start,end) 
            data=array(DataFrame(f[ls_key])).tolist()
            dataFrame[Stock_n[i]]=DataFrame(data)
            print(i,'is done %s' % Stock_n[i])
        except:
            print "ERROR: %s data missing" % Stock_n[i]
            continue
    dataFrame

    del dataFrame['ITB']
    ReturnData=dataFrame.pct_change(1)

    CumulativeReturn=pandas.rolling_apply(ReturnData,90,lambda x: prod(1+x)-1)
    df = CumulativeReturn.iloc[-1:]


    d = {}
    n = 0
    for ticker in Ticker:
        try:
            d[ticker] = df[ticker].tolist()[0]
        except: 
            n += 1        
            print "ERROR: %s data missing" % ticker


    assert n + len(d) == len(Ticker)

    #sort the dictinary in ascending order
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))
    pprint.pprint(sorted_d, width=1)

    data_len = len(Ticker) / 100

    result = sorted_d[-data_len:]

    #convert the result from a list of tuple to a list
    list_result = []
    for res in result:
        list_result.append(res[0])

    print list_result


 

    #write dict to json file
    # in asending order, which means the last one is the largest
    portfolio_dict = {}
    portfolio_dict['portfolio'] = list_result
    portfolio_dict['_comment'] = "NOTE: the last ticket has the highest return"
    filename = DATA_FOLDER + "/data-%s.json" % datetime.datetime.now()
    
    

    # # find the latest file for the latest portfolio
    # # then compare to see what tickers are duplicated
    # os.chdir(DATA_FOLDER)
    # files = []
    # for f in glob.glob("*.json"):
    #     files.append(f)
    


    # latest_file = find_latest_file(files)
    # if latest_file != None:
    #     with open(latest_file) as f:
    #         latest_portfolio = json.load(f)
    #         f.close()

    #     duplicate_ticker_list = []
    #     for portfolio in portfolio_dict:
    #         if portfolio in latest_portfolio:
    #             duplicate_ticker_list.append(portfolio)
    #     portfolio_dict['duplicate'] = duplicate_ticker_list 
    
    # # write portfolio into json file 
    # with open(filename, 'w') as fp:
    #     json.dump(portfolio_dict, fp)




def find_latest_file(files):
    latest_file = None
    latest_time = datetime.datetime(1900,1,1)

    for file_name in files:
        start_index = len("/data")
        end_index = len(".json")
        time = datetime.datetime.strptime(file_name[start_index: -end_index], '%Y-%m-%d %H:%M:%S.%f')

        if time > latest_time:
            latest_file = file_name
            latest_time = time

    return latest_file

if __name__ == "__main__":
    main()