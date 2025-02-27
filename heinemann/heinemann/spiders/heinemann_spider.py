import scrapy
from heinemann.items import HeinemannItem

class HeinemannSpider(scrapy.Spider):
    name = "heinemannspider"

    start_urls = ["https://www.heinemann.com.au/en/sydt1/", "https://www.heinemann-shop.com/en/global/", "https://www.taxfree-heinemann.dk/en/global/"]

    def parse(self, response):
        brands = response.css(".c-header-navigation__col-item a::attr(href)").getall()
        
        for brand in brands:
            if brand.startswith("http") or brand.startswith("/"):
                url=response.urljoin(brand)
                yield response.follow(url, self.brand_page)

    def brand_page(self, response):
        product_urls = response.css("div.c-product-card a::attr(href)").getall()

        for product_url in product_urls:
            if product_url.startswith("http") or product_url.startswith("/"):
                url=response.urljoin(product_url)
                yield response.follow(url, self.product_page)
        
        next_page_url = response.css("ul.c-pagination-bar li a::attr(href)").getall()

        next_page = response.urljoin(next_page_url[-1]) if len(next_page_url)>1 else None

        if next_page:
            yield response.follow(next_page, self.brand_page)


    def product_page(self, response):
            item = HeinemannItem()

            item["product_url"] = response.url
            item["brand_name"] = response.css("div.c-order-card__header h2.c-order-card__subline a::text").get() or ""
            item["brand_url"] = response.urljoin(response.css("div.c-order-card__header h2.c-order-card__subline a::attr(href)").get() or "")
            item["product_name"] = (response.css(".c-order-card__headline::text").get() or "").strip()
            item["quantity"] = response.css("div#product-order-card>p::text").get() or ""
            item["price"] = (response.css("div#product-order-card p.c-price::text").get() or "").strip()
            item["price_per_quantity"] = (response.css("div#product-order-card p.c-price-box__reference::text").get() or "").strip()
            item["stock_availability"] = (response.css("p.c-stock-display>span::text").get() or "").strip()
            item["description"] = (response.css("div.c-accordion__content p:nth-of-type(2)::text").get() or "").strip()

            primary_image_url = response.css("div.c-product-preview__slide img::attr(src)").get()
            item["primary_image"] = response.urljoin(primary_image_url) if primary_image_url else ""

            item["product_images"] = [response.urljoin(img) for img in response.css("div.c-product-preview__thumbnails img::attr(src)").getall()]

            yield item