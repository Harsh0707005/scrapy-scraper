import scrapy
import json
from frankfurt.items import FrankfurtItem

class FrankfurtSpider(scrapy.Spider):
    name = "frankfurtspider"

    start_urls = ["https://shop.frankfurt-airport.com/en-US/brands"]

    def parse(self, response):
        brands = [brand.lower().replace("&", "and").replace(" ", "-").replace("'", "-").replace(".", "") for brand in response.css("li.BrandIndexItem_listItem__RIwm1 *::text").getall()]

        for brand in brands:
            yield response.follow(f"https://shop.frankfurt-airport.com/en-US/search?brandCode={brand}&productAll=true", self.brand_page)
    
    def brand_page(self, response):
        products = response.css("div.ProductTile_productTileWrapper__j70yX > a::attr(href)").getall()

        for product in products:
            yield response.follow(response.urljoin(product), self.product_page)
        
        next_page = response.css("a.Pagination_nextPage__KJaG4::attr(href)").get()

        if next_page:
            yield response.follow(response.urljoin(next_page), self.brand_page)
    
    def product_page(self, response):
        item = FrankfurtItem()

        item["site_name"] = "Frankfurt Airport"
        item["product_id"] = response.url[response.url.rfind("/")+1:]
        item["product_name"] = (response.css("div.ProductHeader_productHeader__JqwPV > h1::text").get() or "").strip().encode("ascii", "ignore").decode()
        item["product_unique_id"] = ""
        item["product_brand_name"] = (response.css("span.ProductHeader_brand__yOd6d > a::text").get() or "").strip().encode("ascii", "ignore").decode()
        item["product_description"] = response.css("div.ProductDescription_description__vcOGj *::text").get(default="").strip()
        item["product_price"] = (response.css("div.ProductPriceRaw_actualPrice__U7PIE::text").get() or "").strip()
        item["product_url"] = response.url
        item["product_images"] = [response.css("img.ProductImage_image__8fRzp::attr(src)").get(default="")]
        item["product_country"] = dict({
            "country_id": "83",
            "country_name": "Germany",
            "country_code": "DE",
            "currency": "EUR",
            "currency_symbol": "€",
            "mobile_code": "+49"
        })
        item["product_category"] = "Duty Free"
        item["product_subcategory"] = "fttb"

        # item["brand_url"] = response.urljoin(response.css("span.ProductHeader_brand__yOd6d > a::attr(href)").get())
        # item["retailer_name"] = (response.css("span.ProductHeader_retailer__kTw1D > a::text").get() or "").strip().encode("ascii", "ignore").decode()
        # item["retailer_url"] = response.urljoin(response.css("span.ProductHeader_retailer__kTw1D > a::attr(href)").get())
        # item["price_per_quantity"] = " ".join([chunk.strip() for chunk in response.css("div.ProductActiveBasePrice_activeBasePrice__4KHlO *::text").getall()])

        # additional_dt = (response.css("dl.ProductAttributes_productAttributes__ERdVr > dt::text").getall())
        # additional_dd = response.css("dd.ProductAttributes_label__e7iXm *::text").getall()

        # item["additional_information"] = json.dumps(dict(zip(additional_dt, additional_dd)), indent=4)

        yield item