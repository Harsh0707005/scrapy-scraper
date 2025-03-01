# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FrankfurtItem(scrapy.Item):
    product_name = scrapy.Field()
    brand_name = scrapy.Field()
    brand_url = scrapy.Field()
    retailer_name = scrapy.Field()
    retailer_url = scrapy.Field()
    price = scrapy.Field()
    price_per_quantity = scrapy.Field()
    description = scrapy.Field()
    additional_information = scrapy.Field()