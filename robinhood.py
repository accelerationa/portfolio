from pandas import *
from numpy import *
import time
from pandas_datareader import data as pdr
from pandas_datareader import robinhood as rb
import datetime
import threading

dataFrame=DataFrame()
ls_key = 'close_price'
start = datetime.datetime(2017,4,24)
end = datetime.datetime(2018,4,20)

Stock_list=read_table('a.txt')
Stock_list=transpose(array(Stock_list)).tolist()
Stocks=Stock_list[0]

n = 0
for stock in Stocks:
    try:
        f = rb.RobinhoodHistoricalReader([stock], start=start,end=end)
        data = f.read()
        data.to_csv('./stocks/' + stock + '.csv')
        print 'Succeeded pulling %s data' % stock
    except Exception as e:
        print 'Failed pulling %s data' % stock
        print e
        pass
    finally: 
        n += 1
        print str(n) + '/' + str(len(Stocks)) + ' done'
        