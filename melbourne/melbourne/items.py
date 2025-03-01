# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MelbourneItem(scrapy.Item):
    product_name = scrapy.Field()
    brand_name = scrapy.Field()
    sku_id = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    primary_image = scrapy.Field()
    additional_information = scrapy.Field()