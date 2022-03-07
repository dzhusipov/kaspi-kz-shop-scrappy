import scrapy
import json

class KaspiSpider(scrapy.Spider):
    name = "kaspi"

    def start_requests(self):
        urls = [
            'https://kaspi.kz/shop/c/categories/',        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.css('a::attr(href)').extract()

        for link in links:
            if link.startswith('/shop/c/categories/'):
                yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        links = response.css('a::attr(href)').extract()
        
        for link in links:
            if link.startswith('/shop/p/'):
                yield response.follow(link, callback=self.parse_product)  

    def parse_product(self, response):
        selectors = response.xpath('//script//text()').extract()
        for selector in selectors:
            if selector.startswith('window.digitalData.product='):
                json_data = json.loads(selector[27:-1])

        yield {
            'title': json_data['name'],
            'price': json_data['unitPrice'],
            'image_urls': json_data['primaryImage']['medium'],
        }
