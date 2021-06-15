import scrapy
from scrapy.loader import ItemLoader
from products.items import ProductsItem

class RskrfSpyder(scrapy.Spider):
    name = 'rskrf'

    start_urls = ['https://rskrf.ru/ratings/produkty-pitaniya/']

    def parse(self, response):
        self.logger.info('Scraping rskrf')
        categories = response.css("div.category-item")
        for i in categories:
            loader = ItemLoader(item=ProductsItem(), selector=i)
            url = i.css('a::attr(href)').get()
            loader.add_value('category', i.css('span')[1].css('span::text').get()) # Добавляем название категории
            item = loader.load_item()
            yield response.follow(url, callback=self.parse_category, meta={'item': item})

    
    def parse_category(self, response):
        item = response.meta['item'].copy()
        loader = ItemLoader(item=item, response=response)
        subcategories = response.css('div.category-item')
        for i in subcategories:
            url = i.css('a::attr(href)').get()
            loader.add_value('subcategory', i.css('span.d-xl-none.d-block::text').get()) # Добавляем подкатегорию
            item = loader.load_item()
            yield response.follow(url, callback=self.parse_subcategory, meta={'item': item})

    
    def parse_subcategory(self, response):
        item = response.meta['item']
        urls = response.css('a')
        for url in urls:
            href = url.css('a::attr(href)').get()
            if href is not None and 'goods' in href:
                yield response.follow(url, callback=self.parse_item, meta={'item': item})
        # next_url в rskrf найти не удалось
        # next_url = response.css('a.page-num.page-item.last::attr(href)').get() 
        # self.logger.info(f'Next url: {next_url}')
        # if next_url is not None:
        #     yield response.follow(next_url, self.parse_subcategory, meta={'item': item})


    def parse_item(self, response):
        item = response.meta['item'].copy()
        loader = ItemLoader(item=item, response=response)
        title = ''
        if len(response.css('p.product-subtitle')) > 0:
            title = response.css('p.product-subtitle::text').get()
        elif len(response.css('h1.h1.product-title')) > 0:
            title = response.css('h1.h1.product-title::text').get()

        loader.add_value('title', title)
    
        ratings = {i.css('span::text')[0].get(): i.css('span::text')[1].get() for i in response.css('div.rating-item')}

        param_1 = [value for key, value in ratings.items() if 'Общий рейтинг' in key]
        if len(param_1) > 0:
            loader.add_value('rate', param_1[0])

        param_2 = [value for key, value in ratings.items() if 'безопасн' in key.lower()]
        if len(param_2) > 0:
            loader.add_value('safety', param_2[0])

        param_3 = [value for key, value in ratings.items() if 'качество' in key.lower()]
        if len(param_3) > 0:
            loader.add_value('quality', param_3[0])

        loader.add_value('source', 'rskrf')
        
        yield loader.load_item()


#
    def parse_item_debug(self, response):
        """Debug sample"""
        """Using (single line in terminal): scrapy parse
        --spider=rskrf
        --loglevel=DEBUG
        -c parse_item_debug 
        "https://rskrf.ru/goods/makaronnye-izdeliya-iz-tverdykh-sortov-pshenitsy-gruppa-a-vysshiy-sort-penne-rigate-penne-rigate-bar/"
        """
        title = ''
        if len(response.css('p.product-subtitle')) > 0:
            title = response.css('p.product-subtitle::text').get()
        elif len(response.css('h1.h1.product-title')) > 0:
            title = response.css('h1.h1.product-title::text').get()

        self.logger.info(f'title: {title}')
    
        ratings = {i.css('span::text')[0].get(): i.css('span::text')[1].get() for i in response.css('div.rating-item')}

        self.logger.info(f'ratings: {ratings}')

        param_1 = [value for key, value in ratings.items() if 'Общий рейтинг' in key]
        if len(param_1) > 0:
            self.logger.info(f'rate: {param_1[0]}')

        param_2 = [value for key, value in ratings.items() if 'безопасн' in key.lower()]
        if len(param_2) > 0:
            self.logger.info(f'safety: {param_2[0]}')

        param_3 = [value for key, value in ratings.items() if 'качество' in key.lower()]
        if len(param_3) > 0:
            self.logger.info(f'quality: {param_3[0]}')
