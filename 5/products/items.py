# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst

def parse_rate(rate):
    """Возвращает число либо None"""
    if rate.strip().replace('.','',1).isdigit():
        return rate.strip()
    else:
        return None


class ProductsItem(Item):
    category = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    subcategory = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    rate = Field(
        input_processor=MapCompose(parse_rate),
        output_processor=TakeFirst()
    )
    safety = Field(
        input_processor=MapCompose(parse_rate),
        output_processor=TakeFirst()
    )
    quality = Field(
        input_processor=MapCompose(parse_rate),
        output_processor=TakeFirst()
    )
    source = Field(
        output_processor=TakeFirst()
    )
