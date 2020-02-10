from pycoder.items import PycoderItem

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
        item = PycoderItem()

        item['title'] = response.css('div.col-sm-9 h2::text').get()
        item['body'] = response.css('div.block-paragraph p::text').get()
        item['date'] = response.css('div.col-sm-9 p::text').get()

        yield item