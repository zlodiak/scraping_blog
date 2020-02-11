from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def add_symbols(text):
    text = '======' + text
    return text

def del_quotes(text):
    text = text.replace('\"', '')
    return text    


class PycoderItem(Item):
    title = Field(
        input_processor=MapCompose(add_symbols, del_quotes),
        output_processor=TakeFirst()    	
    )
    body = Field()
    date = Field()