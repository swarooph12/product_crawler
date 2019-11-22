# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductPriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name=scrapy.Field()
    price=scrapy.Field()
    image_url=scrapy.Field()
    product_rating=scrapy.Field()
    source=scrapy.Field()
