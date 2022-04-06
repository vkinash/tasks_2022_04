# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComputerItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    reviews = scrapy.Field()
    video_card = scrapy.Field()
    video_memory = scrapy.Field()
    processor = scrapy.Field()
    number_of_cores = scrapy.Field()
    ram = scrapy.Field()
    ssd = scrapy.Field()
    hdd = scrapy.Field()
    motherboard = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
