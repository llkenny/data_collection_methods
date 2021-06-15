import scrapy
from scrapy.http import HtmlResponse
from lerua.items import LeruaItem
from scrapy.loader import ItemLoader

class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/kresla-dlya-dachi/']

    # Search init
    # def __init__(self, mark):
    # 	self.start_urls = [f'https://leroymerlin.ru/search?q={mark}']

    def parse(self, response):
        for url in response.css('a'):
            href = url.css('a::attr(href)').get()
            if href is not None and '/product/' in href:
                yield response.follow(url, callback=self.parse_item)

    
    def parse_item(self, response):
        loader = ItemLoader(item=LeruaItem(), response=response)
        loader.add_css('name', 'h1.header-2::text')
        loader.add_css('price', '.primary-price span::text')
        loader.add_xpath('photos', '//picture[contains(@slot, "pictures")]//img/@src')
        yield loader.load_item()
