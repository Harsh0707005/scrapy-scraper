import scrapy
from pathlib import Path
from scrapy.selector import Selector
from aelia.items import AeliaItem

class AeliaSpider(scrapy.Spider):
    name = "aeliaspider"

    start_urls = ["https://www.aeliadutyfree.co.nz/auckland/all-brands", "https://www.aeliadutyfree.co.nz/christchurch/all-brands", "https://www.aeliadutyfree.co.nz/queenstown/all-brands", "https://www.aeliadutyfree.com.au/adelaide/all-brands", "https://www.aeliadutyfree.com.au/cairns/all-brands"]

    def parse(self, response):
        brands = response.css("div.brands-item a")

        for brand in brands:
            brand_name = brand.css("::text").get()
            brand_url = brand.attrib["href"]

            yield response.follow(brand, self.brand_page, meta={"brand_name": brand_name, "brand_url": brand_url})

    def brand_page(self, response):
        products = response.css("a.product::attr(href)").getall()

        for product in products:
            yield response.follow(product, self.product_page, meta={"brand_name": response.meta.get("brand_name", ""), "brand_url": response.meta.get("brand_url", "")})

        next_page = response.css("li.pages-item-next a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, self.brand_page, meta={"brand_name": response.meta.get("brand_name", ""), "brand_url": response.meta.get("brand_url", "")})



    def product_page(self, response):
        item = AeliaItem()

        item["brand_name"] = response.meta.get("brand_name", "").strip()
        item["brand_url"] = response.meta.get("brand_url", "").strip()
        item["product_url"] = response.url
        item["product_name"] = (response.css("h1.page-title span::text").get() or "").strip()
        item["sku_id"] = (response.css("div.sku div::text").get() or "").strip()
        item["description"] = (response.css("div.description div.value div::text").get() or "").strip()
        item["stock_availability"] = (response.css("div.product-info-main div.stock span::text").get() or "").strip()
        item["price"] = (response.css("div.product-info-price span.price::text").get() or "").strip()
        item["image"] = (response.css("div.gallery-placeholder img::attr(src)").get() or "").strip()

        yield item