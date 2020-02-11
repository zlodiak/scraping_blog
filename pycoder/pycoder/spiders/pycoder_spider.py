from pycoder.items import PycoderItem
from scrapy.loader import ItemLoader

import scrapy
from urllib.parse import urljoin


class PycoderSpider(scrapy.Spider):
    name = "pycoder"
    start_urls = ['http://pycoder.ru/?page=1',]
    visited_urls = []

    def parse(self, response):
        if response.url in self.visited_urls:
            return

        self.visited_urls.append(response.url)

        for post_link in response.css('div.post.mb-2 h2 a::attr(href)').getall():
            url = urljoin(response.url, post_link)
            yield response.follow(url, callback=self.parse_post)

        next_pages = response.css('li.page-item:not(.active) a::attr(href)').getall()
        next_page = next_pages[-1]
        next_page_url = urljoin(response.url+'/', next_page)

        yield response.follow(next_page_url, callback=self.parse)

    def parse_post(self, response):
        loader = ItemLoader(item=PycoderItem(), selector=response)

        loader.add_css('title', 'div.col-sm-9 h2::text')
        loader.add_css('body', 'div.block-paragraph p::text')
        loader.add_css('date', 'div.col-sm-9 p::text')

        yield loader.load_item()