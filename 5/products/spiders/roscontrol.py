import scrapy
from scrapy.loader import ItemLoader
from products.items import ProductsItem

class RoscontrolSpyder(scrapy.Spider):
    name = 'roscontrol'

    start_urls = ['https://roscontrol.com/category/produkti/#']

    def parse(self, response):
        self.logger.info('Scraping roscontrol')
        categories = response.css("div.main-container__cont.group")[0].css("a.catalog__category-item.util-hover-shadow")
        for i in categories:
            loader = ItemLoader(item=ProductsItem(), selector=i)
            url = i.css('a::attr(href)').get()
            loader.add_css('category', 'div.catalog__category-name::text') # Добавляем название категории
            item = loader.load_item()
            yield response.follow(url, callback=self.parse_category, meta={'item': item})

    
    def parse_category(self, response):
        item = response.meta['item'].copy()
        loader = ItemLoader(item=item, response=response)
        subcategories = response.css('div.testlab-category')[0].css('a.catalog__category-item.util-hover-shadow')
        for i in subcategories:
            url = i.css('a::attr(href)').get()
            loader.add_value('subcategory', i.css('div.catalog__category-name::text').get()) # Добавляем подкатегорию
            item = loader.load_item()
            yield response.follow(url, callback=self.parse_subcategory, meta={'item': item})

    
    def parse_subcategory(self, response):
        item = response.meta['item']
        products = response.css('a.block-product-catalog__item.js-activate-rate.util-hover-shadow.clear')
        for i in products:
            url = i.css('a::attr(href)').get()
            if url is not None:
                yield response.follow(url, callback=self.parse_item, meta={'item': item})
        next_url = response.css('a.page-num.page-item.last::attr(href)').get()
        self.logger.info(f'Next url: {next_url}')
        if next_url is not None:
            yield response.follow(next_url, self.parse_subcategory, meta={'item': item})


    def parse_item(self, response):
        item = response.meta['item'].copy()
        loader = ItemLoader(item=item, response=response)
        loader.add_css('title', 'h1.main-title.testlab-caption-products.util-inline-block::text')
        total_rates = response.css('div.product__single-rev-total')
        if len(total_rates) > 0:
            loader.add_css('rate', 'div.total::text')
    
        ratings = {i.css('div.rate-item__title::text').get(): i.css('span::text').get() for i in response.css('div.rate-item.group')}

        param_2 = [value for key, value in ratings.items() if 'безопасн' in key.lower()]
        if len(param_2) > 0:
            loader.add_value('safety', param_2[0])

        param_3 = [value for key, value in ratings.items() if 'качество' in key.lower()]
        if len(param_3) > 0:
            loader.add_value('quality', param_3[0])

        loader.add_value('source', 'roscontrol')

        yield loader.load_item()
