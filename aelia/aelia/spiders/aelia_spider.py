import scrapy
from pathlib import Path
from scrapy.selector import Selector
from aelia.items import AeliaItem
from urllib.parse import urlparse
import json

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

        item["site_name"] = "Aelia"
        item["product_id"] = response.url[response.url.rfind("/")+1:-5]
        item["product_name"] = (response.css("h1.page-title span::text").get() or "").strip()
        item["product_unique_id"] = (response.css("div.sku div::text").get() or "").strip()
        item["product_brand_name"] = response.meta.get("brand_name", "").strip()
        item["product_description"] = (" ".join(response.css("div.description div.value *::text").getall())).strip()
        item["product_price"] = (response.css("div.product-info-price span.price::text").get() or "").strip()
        item["product_url"] = response.url
        item["product_images"] = [(response.css("div.gallery-placeholder img::attr(src)").get() or "").strip()]

        country_code = urlparse(response.url).netloc.split(".")[-1]

        with open("country_data.json", "r") as f:
            countries = json.load(f)["countries"]
            for country in countries:
                if country["country_code"].lower()==country_code.lower():
                    country_data = country
        
        item["product_country"] = country_data

        item["product_category"] = "Duty Free"
        item["product_subcategory"] = "fttb"



        # item["brand_url"] = response.meta.get("brand_url", "").strip()
        # item["stock_availability"] = (response.css("div.product-info-main div.stock span::text").get() or "").strip()

        yield item