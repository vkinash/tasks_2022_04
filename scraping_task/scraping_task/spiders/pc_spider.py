from csv import writer

import os
import scrapy


class PCSpider(scrapy.Spider):
    name = "pc"
    start_urls = ["https://it-blok.com.ua/computeri.html"]

    if not os.path.exists('output'):
        os.makedirs('output')

    def parse(self, response):
        links = response.css('div.button-group a::attr(href)')
        yield from response.follow_all(links, self.parse_pc)

        next_page = response.css('a.next-pagination::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


    def parse_pc(self, response):
        if response.css('tbody:nth-of-type(7) > tr > td:nth-of-type(1)::text').get()[5:] == 'HDD':
            HDD, SSD = '+', '-'
        else:
            HDD, SSD = '-', '+'

        yield {
            'PC name': response.css('div.pp-m-blok h1::text').get(),
            'Price': response.css('span.autocalc-product-special::text').get(),
            'Reviews': response.css('ul.nav.nav-tabs a::text')[4].re(r'\d')[0],
            'Image': '',
            'Video card': response.css('tbody:nth-of-type(6) > tr:nth-of-type(2) > td:nth-of-type(2)::text').get(),
            'Video memory': response.css('tbody:nth-of-type(6) > tr:nth-of-type(3) > td:nth-of-type(2)::text').get(),
            'Processor': response.css('tbody:nth-of-type(2) > tr:nth-of-type(1) > td:nth-of-type(2)::text').get(),
            'Number of cores': response.css('tbody:nth-of-type(2) > tr:nth-of-type(4) > td:nth-of-type(2)::text').get(),
            'RAM': response.css('tbody:nth-of-type(5) > tr:nth-of-type(1) > td:nth-of-type(2)::text').get(),
            'SSD': SSD,
            'HDD': HDD,
            'Motherboard': response.css('tbody:nth-of-type(4) > tr > td:nth-of-type(2)::text').get(),
            }

