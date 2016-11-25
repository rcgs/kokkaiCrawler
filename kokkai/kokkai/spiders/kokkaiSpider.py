
from kokkai.items import kokkaiItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from lxml import  html
from scrapy import log
from datetime import datetime
from datetime import date
import scrapy
import pymysql.cursors
from scrapy import log
from pprint import pprint
import  re
import os

class kokkaiSpider(scrapy.Spider):
    name = "kokkai"
    allowed_domains = ["iss.ndl.go.jp",
    "ndlopac.ndl.go.jp",
    "id.ndl.go.jp"
    ]

    start_urls = []
        #"http://iss.ndl.go.jp/books/R100000002-I000004356337-00"
    
    #start_urls=["https://itunes.apple.com/jp/genre/ios-gemu/id6014?letter=R&mt=8&page=5"]
    #rules = [Rule(LinkExtractor(),callback='parse_data)]
    
    def __init__(self,*args,**kwargs):
        super(kokkaiSpider, self).__init__(*args,**kwargs)

        urls = None
        with open(os.getcwd() + "\\kokkailist.txt","r") as f:
            urls = f.readlines()
            

        self.start_urls = [url.rstrip("\n") for url in urls if url != "\n"]
        #log.msg("starts is "+pprint(self.start_urls),_level=logging.DEBUG)
        
    def parse(self, response):
        '''
                self.item["kokkai_link"] = ""
                self.item["shosi_id"] = ""
                self.item["opac_link"] = ""
        '''
        item = item = kokkaiItem()

        link = response.xpath('//div[2]/div[@class ="servicebox"]/ul[@style = "margin-bottom: 0px;"]/li/a/@href').extract()
        link = self.fair_str(link)
        item["kokkai_link"] = response.url
        
        request = scrapy.Request(url=link,callback=self.parse_page)
        request.meta["item"] = item
        return request
        
        '''
        xpath_next = "//div[2]/ul[2]/li/a[@class='paginate-more']/@href"
        nextpage = response.xpath(xpath_next).extract()
        next=nextpage
        #log.msg("nextpage is" + nextpage, levenl=log.DEBUG)
        if nextpage :
            next_url = str(nextpage)
            next_url = re.sub(r"[~\[\']", "", next_url)
            next_url = re.sub(r"[\'\]$]", "", next_url)
            request = scrapy.Request(url=next_url)
            yield request
        '''
 



    def parse_page(self, response):
        #for sel in response.xpath('//div[@id="main"]'):
        #self.SerialID=self.get_ID(100,"AP")
        item = response.meta["item"]

        item["shosi_id"] = "'"+self.fair_str(item["kokkai_link"],self.regexp,r"(?<=-I)[0-9]+")+"'"
        #self.item["shosi_id"] = response.xpath('//td[@class ="t-td-full"]/span[@class="text3"]/text()').extract()
        item["opac_link"] = response.url
        log.msg(pprint(item),level=log.DEBUG)
        
        return item




        #for sel in response.xpath('//div[@id="selectedgenre"]//div/ul/li'):
        #    item = appItem()
        #    item['title'] = sel.xpath('a/text()').extract()
        #    item['link'] = sel.xpath('a/@href').extract()

        #    log.msg("WORKING\n", level=log.DEBUG)

        #    yield item

        """
        scrapyのデータを時価で取得すると['   ']という感じで行末行頭に余分な文字が
        発生するため削除を行う関数
        """

    def fair_str(self,string,function=None,regexp=None):
        #余分な文字列を削除

        string = re.sub(r"[~\[\']", "", str(string)) 
        string = re.sub(r"[\'\]$]", "", str(string))
        
        if function is not None and regexp is None:#追加の関数があった場合
            string = function(string) 
        

        if function is not None and regexp is not None:#正規表現のパターンが入力されていた場合
            string =function(string,regexp)
        

        return string 

    def check_none(self,string):
        if string is "":
            string = ";none"
        return string

    def regexp(self,string,regexp):
        match = re.search(regexp,string)
        if match is not None:
            string = match.group()
            log.msg(string,level = log.DEBUG)
        else:
            string = ";none"
        return string
    
    def check_bit(self,string):
        if string is "" :
            return 0
        else:
            return 1
    def check_int(self,string):
        match = re.search(r"[0-9]+",string)
        if match is not None:
            string =match.group() 
            return string
        else:
            string ="0"
            return string

    def check_date(self,string):
        match = re.search(r'[0-9]{4}.[0-9]+.[0-9]+',string)
        re_string = None
        if match is not None:
            re_string = match.group()
            #log.msg(re_string,level=log.DEBUG)
            re_string = re.sub(r"([一-龥])","-",re_string)
            #log.msg(re_string,level=log.DEBUG)
        #else:
            #log.msg(match.group(),level=log.DEBUG)
        return re_string

