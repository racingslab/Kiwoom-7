# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import requests
import time

class btsForReal:
    
    def source(self):
        frame_src = 'http://www.daishin.co.kr/ctx_kr/sc_stock/sg_stock_info/svc_kosdaq_total/KosdaqKsSise.shtml'
        return frame_src
        
    def UrlParsing(self):
        _start=time.time()
#         frame_src = 'http://www.daishin.co.kr/ctx_kr/sc_stock/sg_stock_info/svc_kosdaq_total/KosdaqKsSise.shtml'
        frame_src = self.source()

        self.iframe_content=BeautifulSoup(requests.get(frame_src).content,"lxml")

        self.td = self.iframe_content.find_all("td")


        self.codeNameCoast={}
        for a in self.td:
            if a.a is not None:
                
                if str(a.find("a").contents[0]).startswith('A') ==True:
                    self.inerNameCoast={}
                    coast =a.a.parent.next_sibling.next_sibling.contents[0] #가격 
                    change=a.a.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0] #변화량
                    changePercent = a.a.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.contents[0] #변화퍼센트
                    changePercent = changePercent[0:changePercent.index('%')]
                    
                    code = str(a.find("a").contents[0])[1:7]
                    name = str(a.find("a").contents[0])[8:]
                    
                    self.inerNameCoast[name]=changePercent
                    self.codeNameCoast[code]=self.inerNameCoast
                    del(self.inerNameCoast)
        
        print('DAHSIN PARSING ['+str(time.time()-_start)+']')
#         self.printCodeNameCoast()
        return self.codeNameCoast
        
    def getCodeNameCoast(self):
        return self.codeNameCoast
    
    def printCodeNameCoast(self):
        
        index = 0
#         print(self.codeNameCoast)
        for a in self.codeNameCoast:
            for b in self.codeNameCoast[a]:
                index+=1
                print('name '+str(b)+" coast: "+str(self.codeNameCoast[a][b]) + " code :"+str(a))
        print('all items ['+str(index)+']')
        
    def addZeroToStockCode(self,str):
        str=str.strip()

        if len(str.strip())<=6:
            while(len(str.strip())!=6):
                str=str[:0]+"0"+str[0:]
        return str    
    
        
if __name__=="__main__":

    bfd = btsForReal()
    codeNameCoast = bfd.UrlParsing()
    for code in codeNameCoast:
        for Name in codeNameCoast[code]:
            print('code [ '+str(code)+'] name [ '+str(Name)+' ] 가격  [ '+ str(codeNameCoast[code][Name])+']')
