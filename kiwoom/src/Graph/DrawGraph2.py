# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import matplotlib.finance as fn
import sys
from matplotlib.dates import date2num
sys.path.append('../')
sys.path.append('../Data')
import YGGetWebData
import btsForDaily
import datetime
import time
import pandas as pd


def movingAverage(values,window):
    
    value = pd.Series(values)
    yMa=pd.stats.moments.rolling_mean(value,window)
    return yMa

def checkGolden(ax,dd,SP):
    
    prev_key=prev_val=0
    for key,val in dd['golden_20_5'].iteritems():
        if val ==0:
            continue
        if val*prev_val < 0 and val > prev_val:
            ax.annotate('GOLDEN',xy=(dd['Date'][-SP:][key],dd['Mv20'][key]),xytext=(10,-30),textcoords='offset points',arrowprops=dict(facecolor='red',arrowstyle="->"))
            print(dd['DateIndex'][-SP:][key])
        if val*prev_val < 0 and val < prev_val:
            ax.annotate('DEAD',xy=(dd['Date'][-SP:][key],dd['Mv20'][key]),xytext=(10,30),textcoords='offset points',arrowprops=dict(facecolor='blue', arrowstyle="->"))
        prev_key,prev_val=key,val
        
def getData(code,date,TIMEOUT="",DATE_FMT=""):
    
    return YGGetWebData.getStockPriceData(code,date,TIMEOUT,DATE_FMT)

def drawGraph(code,date):
    date_fmt = '%Y-%m-%d'
    dd = getData(code,date,date_fmt)
    
    dd['Mv5']=movingAverage(dd['close'],5)
    dd['Mv20']=movingAverage(dd['close'],20)
    dd['golden_20_5']=dd['Mv5']-dd['Mv20']
    
    dd.Date=mdates.date2num(dd.Date.dt.to_pydatetime())
    SP=len(dd[19:])
    fig,ax = plt.subplots()
    
    ax.plot_date(dd['Date'][-SP:],dd['close'][-SP:],'-')
    ax.plot(dd['Date'][-SP:],dd['Mv5'][-SP:],'-',label='5 SMA',linewidth=1)
    ax.plot(dd['Date'][-SP:],dd['Mv20'][-SP:],'-',label='20 SMA',linewidth=1)
    plt.legend(loc='best')

    checkGolden(ax,dd,SP)
        
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt)) # change the date Format
    fig.autofmt_xdate() #neat the date format
    plt.show()
    
if __name__ == '__main__':
    
    drawGraph('021080','2015-06-1')