# -*- coding: utf-8 -*-
import bts
import requests
from bs4 import BeautifulSoup
import datetime


class daily(bts.mbts):
    
#     def __init__(self):
#         pass
    
    def source(self,page="",code=""):
        

        self.url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page='+str(page)+'&code='+str(code)+'&modify=1'   #한페이지에 30일치 나옴. 

        if page=="" or code=="":
            self.url = 'http://finance.daum.net/item/quote_yyyymmdd_sub.daum?page=1&code=035720&modify=1' 
            
    def sourceForForeignAndCompany(self,page="",code=""):
        
        self.urlForFAndC = 'http://finance.daum.net//item/foreign_yyyymmdd.daum?page='+str(page)+'&code='+str(code) 

        if page=="" or code=="":
            self.urlForFAndC = 'http://finance.daum.net//item/foreign_yyyymmdd.daum?page=1&code=035720'         
        
    def parse(self,page,code,start,Timeout,end=""):
        self.source(page,code)
        
        '''시,고,저,종,거래량'''
        readTimout  =Timeout
        ConnectTimeout  =Timeout
        retry = 5
        
        for i in range(retry):    
            try:
                content = requests.get(self.url,timeout=(ConnectTimeout,readTimout)).text
                break
            except requests.exceptions.ConnectTimeout as e:
                print('ConnectTimeout !! count : ',i)
                
                continue
            except requests.exceptions.ReadTimeout as e:
                print ('ReadTimeout!!! count : ' ,i)
                continue
                
        bs4     = BeautifulSoup(content,'lxml')
        price   = bs4.find_all("td",class_="datetime2")
        
        for daily in price:
            
            datePrice       =   daily
            datePrice       =   datePrice.contents[0]
            year_month_day  =   datePrice.split('.')
            datePrice       =   datePrice.replace('.','-')
            datePrice       =   '20'+datePrice
            
            self.dateTime       =   self.getDate(datePrice)
            if self.start > self.dateTime:
                self.Flag=False
                break
            
            year            =   year_month_day[0]
            month           =   year_month_day[1]
            day             =   year_month_day[2]
            
            start_price     =   daily.next_sibling.next_sibling
            high_price      =   start_price.next_sibling.next_sibling
            low_price       =   high_price.next_sibling.next_sibling
            end_price       =   low_price.next_sibling.next_sibling
            volume          =   end_price.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
            
            start_price     =   start_price.contents[0]
            high_price      =   high_price.contents[0]
            low_price       =   low_price.contents[0]
            end_price       =   end_price.contents[0]
            volumn          =   volume.contents[0]
        
            start_price     =   str(start_price).replace(',','')
            high_price      =   str(high_price).replace(',','')
            low_price       =   str(low_price).replace(',','')
            end_price       =   str(end_price).replace(',','')
            volumn          =   str(volumn).replace(',', '')
            
            appendLine = str(datePrice),start_price,high_price,low_price,end_price,volumn
#             self.dailyData[self.index]=str(datePrice),str(end_price),str(volumn)
            self.dailyData[self.index]=appendLine
            
            self.index+=1
                
    def getDataFromDaum(self,code,start,Timeout,end=""):
        '''Format = 16-02-04'''
        '''end default = today'''
        self.dailyData = {}
        self.index = 1
        self.end=datetime.datetime.today()
        
        if end != "":
            self.end = self.getDate(end)
            
            
        end_year = self.end.year
        end_month = self.end.month
        end_day = self.end.day
        
        self.start=self.getDate(start)
        
        start_year = self.start.year
        start_Month = self.start.month
        start_Day = self.start.day
        
        
        page=1
        self.Flag = True
        while self.Flag and page<=10:       
            self.parse(page,code,self.start,Timeout)
            page+=1
        
        return self.dailyData
    
    def getForeignerBuyDaum(self,code,start,Timeout,end=""):
        '''Code = 기관코드
            startDate부터 enddate까지. end는 기본 오늘날짜로 설정.
        '''
        
        self.dailyDataForFAndC = {}
        self.indexForFAndC = 1
        self.endForFAndC=datetime.datetime.today()
        
        if end != "":
            self.endForFAndC = self.getDate(end)
            
        self.startForFAndC=self.getDate(start)    
        
        
        page =1
        self.FlagForFAndC=True
        
        while self.FlagForFAndC and page<=10:
            self.parseForForeignAndCompany(page,code,self.startForFAndC,Timeout)
            page+=1
        
        return self.dailyDataForFAndC
    
    def parseForForeignAndCompany(self,page,code,start,Timeout,end=""):
        self.sourceForForeignAndCompany(page, code)
        
        readTimout = Timeout
        ConnectTimeout = Timeout
        retry = 5
        
        for i in range(retry):
            try:
                content = requests.get(self.urlForFAndC,timeout=(ConnectTimeout,readTimout)).text
                break
            except requests.exceptions.ConnectTimeout as e:
                print('ConnectTimeout !! count : ',i)
                
                continue
            except requests.exceptions.ReadTimeout as e:
                print ('ReadTimeout!!! count : ' ,i)
                continue
            
        bs4     = BeautifulSoup(content,'lxml')
        volume  =  bs4.find_all("td",class_="datetime2")
        
        for Pure in volume:
            
            date    =   str(Pure.contents[0])
            date    =   date.replace('.','-')
            date    =   '20'+date
            
            self.dateTimeForFAndC =   self.getDate(date)
            if self.startForFAndC > self.dateTimeForFAndC:
                self.FlagForFAndC = False
                break
            
            
            ForeignPurBuy = Pure.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
            CompanyBuy  = ForeignPurBuy.next_sibling.next_sibling
            
            ForeignPurBuy =ForeignPurBuy.contents[0]
            CompanyBuy  =CompanyBuy.contents[0]
            
            ForeignPurBuy=str(ForeignPurBuy).replace(',', '')
            CompanyBuy = str(CompanyBuy).replace(',', '')
            
            appendLine = date,ForeignPurBuy,CompanyBuy
            
            self.dailyDataForFAndC[self.indexForFAndC]=appendLine            
            self.indexForFAndC +=1
    
    def getDate(self,Date):
        '''String Format(2014-02-04) return datetime object'''
        
        dmt_Format='%Y-%m-%d'
        
        Date = str(Date)
        
        if not Date.startswith('20'):
            Date = '20'+Date
        
        return datetime.datetime.strptime(str(Date),dmt_Format)
        
        
        
 

if __name__=='__main__':
    
    dd = daily()
#     gd = dd.getDate('99-02-04')
#     print(gd)
#     print(dd.getForeignerBuyDaum('021080','5'))
    
#     print(dd)
    data = dd.getForeignerBuyDaum('126700','2015-2-12',5)
#     data = dd.getDataFromDaum('126700','2015-2-12',5)
    for dd in data:
        date = data[dd][0]
        price= data[dd][1]
        highprice=data[dd][2]
#         lowprice=data[dd][3]
#         endprice =data[dd][4]
#         volume=data[dd][5]
        index = dd
#         print('날짜',date,'시가',price,'고가',highprice,'저가',lowprice,'종가',endprice,'거래량',volume,'순번',index)
        print('date',date,'Foreign',price,'Company',highprice)
#         print(type(date))