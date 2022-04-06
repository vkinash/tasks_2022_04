import scrapy
from scraping_task.items import ComputerItem


class PCSpider(scrapy.Spider):
    name = "pc"
    start_urls = ["https://it-blok.com.ua/computeri.html"]
    base_url = "https://it-blok.com.ua/"

    def parse(self, response):
        links = response.css('div.button-group a::attr(href)')
        yield from response.follow_all(links, self.parse_pc)

    def parse_pc(self, response):
        if response.css('tbody:nth-of-type(7) > tr > td:nth-of-type(1)::text').get()[5:] == 'HDD':
            HDD, SSD = '+', '-'
        else:
            HDD, SSD = '-', '+'

        img_urls_list = [self.base_url + i for i in response.css("a.thumbnail::attr(href)").getall()]

        yield ComputerItem(
            name=response.css('div.pp-m-blok h1::text').get(),
            price=response.css('span.autocalc-product-special::text').get(),
            reviews=response.css('ul.nav.nav-tabs a::text')[4].re(r'\d')[0],
            video_card=response.css('tbody:nth-of-type(6) > tr:nth-of-type(2) > td:nth-of-type(2)::text').get(),
            video_memory=response.css('tbody:nth-of-type(6) > tr:nth-of-type(3) > td:nth-of-type(2)::text').get(),
            processor=response.css('tbody:nth-of-type(2) > tr:nth-of-type(1) > td:nth-of-type(2)::text').get(),
            number_of_cores=response.css('tbody:nth-of-type(2) > tr:nth-of-type(4) > td:nth-of-type(2)::text').get(),
            ram=response.css('tbody:nth-of-type(5) > tr:nth-of-type(1) > td:nth-of-type(2)::text').get(),
            ssd=SSD,
            hdd=HDD,
            motherboard=response.css('tbody:nth-of-type(4) > tr > td:nth-of-type(2)::text').get(),
            image_urls=img_urls_list
        )
