import scrapy
from kingpower.items import KingpowerItem

class KingpowerSpider(scrapy.Spider):
    name = "kingpowerspider"

    start_urls = ["https://www.kingpower.com/en/brands"]

    all_pages_scraped = False

    def parse(self, response):
        brands = response.css("div.brands__BrandContentBoxRight-sc-fr1raq-7 a::attr(href)").getall()

        for brand in brands:
            if brand.startswith("http") or brand.startswith("/"):
                yield response.follow(response.urljoin(brand), self.brand_page)
        
    def brand_page(self, response):
        product_urls = response.css("div.MuiGridItem-root a::attr(href)").getall()
    
        brand_name = (response.css("span#brand-page-product-list-result-header::text").get() or "").strip()
        brand_url = response.url

        for product_url in product_urls:
            if product_url.startswith("http") or product_url.startswith("/"):
                yield response.follow(response.urljoin(product_url), self.product_page, meta={"brand_name": brand_name, "brand_url": brand_url})
        
        
        if (not self.all_pages_scraped):
            numPages = len(response.css("ul#pagination-wrapper li").getall())

            self.all_pages_scraped = True

            for i in range(1,numPages+1):
                yield response.follow(f"{response.url}?page={i}", self.brand_page)
            

    def product_page(self, response):

        item = KingpowerItem()

        item["brand_name"] = response.meta.get("brand_name", "")
        
        item["brand_url"] = response.meta.get("brand_url", "")

        item["product_url"] = response.url

        item["name"] = (response.css("h4#product-detail-title-product-name::text").get() or "").strip()

        item["description"] = " ".join(response.css("div#product-detail-long-description-paragraph *::text").getall()).strip()

        item["categories"] = (response.css("div.MuiBreadcrumb-breadcrumb span::text").getall())[1:]

        item["sku_id"] = (response.css("span#product-detail-sku-number::text").getall())[-1].strip()

        item["price"] = (response.css("span#product-detail-label-product-price::text").get() or "").strip()

        item["primary_image"] = (response.css("img#product-slider-image-1::attr(src)").get() or "").strip()

        item["images"] = response.css("div.slick-slide img::attr(src)").getall()

        yield item