# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeinemannItem(scrapy.Item):
    product_url = scrapy.Field()
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
    product_name = scrapy.Field()
    quantity = scrapy.Field()
    price = scrapy.Field()
    price_per_quantity = scrapy.Field()
    stock_availability = scrapy.Field()
    description = scrapy.Field()
    primary_image = scrapy.Field()
    images = scrapy.Field()