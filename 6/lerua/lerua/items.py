# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def get_price(value):
    value = value.strip().replace(' ','',1)
    try:
        return float(value)
    except:
        return None


class LeruaItem(Item):

    _id = Field()
    name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    photos = Field()
    price = Field(
        input_processor=MapCompose(get_price),
        output_processor=TakeFirst()
    )
    