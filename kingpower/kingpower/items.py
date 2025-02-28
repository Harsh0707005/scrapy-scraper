# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KingpowerItem(scrapy.Item):
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    sku_id = scrapy.Field()
    price = scrapy.Field()
    primary_image = scrapy.Field()
    images = scrapy.Field()