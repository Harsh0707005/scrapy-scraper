# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AeliaItem(scrapy.Item):
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    sku_id = scrapy.Field()
    description = scrapy.Field()
    stock_availability = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()