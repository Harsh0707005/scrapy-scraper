# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HeinemannItem(scrapy.Item):
    site_name = scrapy.Field()
    product_id= scrapy.Field()
    product_name = scrapy.Field()
    product_unique_id = scrapy.Field()
    product_brand_name = scrapy.Field()
    product_description = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_images = scrapy.Field()
    product_country = scrapy.Field()
    product_subcategory = scrapy.Field()
    product_category = scrapy.Field()
    # product_url = scrapy.Field()
    # brand_name = scrapy.Field()
    # brand_url = scrapy.Field()
    # product_name = scrapy.Field()
    # quantity = scrapy.Field()
    # price = scrapy.Field()
    # price_per_quantity = scrapy.Field()
    # stock_availability = scrapy.Field()
    # description = scrapy.Field()
    # primary_image = scrapy.Field()
    # images = scrapy.Field()