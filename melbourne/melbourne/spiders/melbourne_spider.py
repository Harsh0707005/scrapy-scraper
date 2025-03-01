import scrapy
import json
from melbourne.items import MelbourneItem

class MelbourneSpider(scrapy.Spider):
    name = "melbournespider"

    start_urls = ["https://laneway.melbourneairport.com.au/all-products"]

    def parse(self, response):
        products = list(set((response.selector.xpath('//*[@id="amasty-shopby-product-list"]/div[2]/ol')).css("a::attr(href)").getall()))

        for product in products:
            yield response.follow(product, self.product_page)
        
        next_page = response.css("li.pages-item-next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def product_page(self, response):
        item = MelbourneItem()
    
        item["product_name"] = (response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[2]/h1/span/text()').get() or "").strip()
        item["brand_name"] = (response.css("span.brand-name::text").get() or "").strip()
        item["sku_id"] = (response.xpath('//*[@id="maincontent"]/div[2]/div/div[3]/div[3]/div[2]/div/text()').get() or "").strip()
        item["price"] = (response.css("span.price::text").get() or "").strip()
        item["description"] = " ".join(response.css("div#description *::text").getall()).strip()
        item["primary_image"] = (response.css("div.gallery-placeholder img::attr(src)").get() or "").strip()
        
        additional_th = response.css("div#additional th::text").getall()
        additional_td = response.css("div#additional td::text").getall()
        item["additional_information"] = json.dumps(dict(zip(additional_th, additional_td)), indent=4)
        
        yield item