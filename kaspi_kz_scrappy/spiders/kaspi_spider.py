import scrapy

class KaspiSpider(scrapy.Spider):
    name = "kaspi"

    def start_requests(self):
        urls = [
            'https://kaspi.kz/shop/c/categories/',        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get all links from response
        links = response.css('a::attr(href)').extract()

        self.log('123412341234123412341234123412341234')
        for link in links:
            if link.startswith('/shop/c/categories/'):
                self.log(f'link {link}')
                yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        # get all links from response
        links = response.css('a::attr(href)').extract()
        for link in links:
            if link.startswith('/shop/p/'):
                yield response.follow(link, callback=self.parse_product)  

    def parse_product(self, response):
        # print response
 
        title = response.css('item__heading::text').extract_first()
        price = response.css('div.item__price-once::text').get()
        description = response.css('div.product-description::text').extract_first()
        image_url = response.css('img.product-image::attr(src)').extract_first()
        print(f'{title} {price} {description} {image_url}')
        self.log(f'title {title}')
        self.log(f'price {price}')
        self.log(f'description {description}')
        self.log(f'image_url {image_url}')

        #yield {
        #    'title': response.css('h1::text').extract_first(),
        #    'price': response.css('span.price::text').extract_first(),
        #    'description': response.css('div.description::text').extract_first(),
        #    'image_urls': response.css('img::attr(src)').extract(),
        #}

        #page = response.url.split("/")[-2]
        #filename = f'quotes-{page}.html'
        #with open(filename, 'wb') as f:
        #   f.write(response.body)
        #self.log(f'Saved file {filename}')