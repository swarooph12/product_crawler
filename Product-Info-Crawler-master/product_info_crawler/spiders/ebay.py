# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import re
from ..items import ProductPriceItem

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  raw_html.encode('ascii','ignore')
  cleantext = re.sub(cleanr, '', raw_html)
  cleantext=cleantext.strip()
  cleantext=re.sub('\s+',' ',cleantext)
  return cleantext

class EbaySpider(CrawlSpider):
    name = 'ebay'
    def __init__(self, product='apple', domain=None, *args, **kwargs):
        super(EbaySpider, self).__init__(*args, **kwargs)
        self.product_name=product.lower()
        self.product_name=re.sub("[^ a-zA-Z0-9]+", "", self.product_name)
        self.search_url='https://www.ebay.in/sch/i.html?_ipg=25&_nkw='+self.product_name
        self.allowed_domains = ['www.ebay.in']
        self.start_urls = [self.search_url]

    rules = (
      Rule(LinkExtractor(allow=(), tags=('a'),attrs=('href'),restrict_css=('.next',)),
           callback="parse_items",
           follow=True),)

    def parse_start_url(self,response):
        request=Request("https://www.ebay.in/sch/i.html?_ipg=25&_nkw=", callback=self.parse_items)
        return request

    
    def parse_items(self, response):
       print ('Processing...',response.url)
       title=[]
       image=[]
       price=[]
       rating=[]
       for item in response.xpath("//a[@class='item__link']").xpath("@href").getall():
         item_title=item.xpath("//h1[@id='itemTitle']//text()").get()
         item_image=item.xpath("//img[@id='icImg']").xpath("@src").get()
         item_price=item.xpath("//span[@id='prcIsum']//text()").get()
         item_rating=item.xpath("//div[@id='vi-itm-cond']//text()").get()
         if(item_title and item_image and item_price and item_rating):
          title.append(cleanhtml(item_title))
          image.append(cleanhtml(item_image))
          price.append(cleanhtml(item_price))
          url.append(cleanhtml(item_rating))

       print ('Result Counts: ',len(title))
       
       for item in zip(title,price,image,url):
           scraped_info = {
               'product_name' : item[0],
               'price' : item[1],
               'image_url' : item[2],
               'product_rating': item[3],
               'source': 'ebay.in' 
           }

           yield scraped_info