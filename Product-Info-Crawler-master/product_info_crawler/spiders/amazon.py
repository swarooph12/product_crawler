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

class AmazonSpider(CrawlSpider):
    name = 'amazon'
    def __init__(self, product='apple', domain=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.product_name=product.lower()
        self.product_name=re.sub("[^ a-zA-Z0-9]+", "", self.product_name)
        self.search_url='https://www.amazon.com/s?k='+self.product_name
        self.allowed_domains = ['www.amazon.com']
        self.start_urls = [self.search_url]

    rules = (
          Rule(LinkExtractor(allow=(), tags=('a'),attrs=('href'),restrict_css=('.pagnNext',)),
               callback="parse_items",
               follow=True),)

    def parse_start_url(self,response):
        request=Request("https://www.amazon.com/s?k=", callback=self.parse_items)
        return request

    def parse_items(self, response):
       print ('Processing...',response.url)
       title=[]
       image=[]
       price=[]
       rating=[]
       for item in response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall():

         item_title=item.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
         item_image=item.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get()
         item_price=item.xpath("//span[@id='priceblock_ourprice']//text()").get() or response.xpath("//span[@id='priceblock_dealprice']//text()").get()
         item_rating = item.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath("//span[@class='a-icon-alt']//text()").get()
         if(item_title and item_image and item_price and item_rating):
          title.append(cleanhtml(item_title))
          image.append(cleanhtml(item_image))
          price.append('Rs. '+ cleanhtml(item_price))
          rating.append(cleanhtml(item_rating))
       print ('Result Counts: ',len(title))
       
       for item in zip(title,price,image,rating):
           scraped_info = {
               'product_name' : item[0],
               'price' : item[1],
               'image_url' : item[2],
               'product_rating': item[3],
               'source': 'amazon.in' 
               }
           yield scraped_info