from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def add_symbols(text):
    text = '======' + text
    return text


class PycoderItem(Item):
    title = Field(
        input_processor=MapCompose(add_symbols),
        output_processor=TakeFirst()    	
    )
    body = Field()
    date = Field()