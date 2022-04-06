import csv
import hashlib

from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapingTaskPipeline(ImagesPipeline):

    def process_item(self, item, spider):
        # calling dumps to create json data.
        # ram = re.findall('\d+', item['RAM'])[0]
        ram = item['ram']
        item['image_urls'] = '|'.join([i['path'] for i in item['images']])
        del(item['images'])
        line = self.get_writer(ram)
        line.writerow(item)
        return item

    def open_spider(self, spider):
        field_names = [
            'name',
            'price',
            'reviews',
            'video_card',
            'video_memory',
            'processor',
            'number_of_cores',
            'ram',
            'ssd',
            'hdd',
            'motherboard',
            'image_urls'
        ]

        self.file_4 = open('output/4gb.csv', 'w')
        self.dict_writer_4 = csv.DictWriter(self.file_4, fieldnames=field_names)
        self.dict_writer_4.writeheader()

        self.file_8 = open('output/8gb.csv', 'w')
        self.dict_writer_8 = csv.DictWriter(self.file_8, fieldnames=field_names)
        self.dict_writer_8.writeheader()

        self.file_16 = open('output/16gb.csv', 'w')
        self.dict_writer_16 = csv.DictWriter(self.file_16, fieldnames=field_names)
        self.dict_writer_16.writeheader()

        self.file_32 = open('output/32gb.csv', 'w')
        self.dict_writer_32 = csv.DictWriter(self.file_32, fieldnames=field_names)
        self.dict_writer_32.writeheader()

        self.file_64 = open('output/64gb.csv', 'w')
        self.dict_writer_64 = csv.DictWriter(self.file_64, fieldnames=field_names)
        self.dict_writer_64.writeheader()

        self.file_fail = open('output/fail.csv', 'w')
        self.dict_writer_fail = csv.DictWriter(self.file_fail, fieldnames=field_names)
        self.dict_writer_fail.writeheader()

    def close_spider(self, spider):
        self.file_4.close()
        self.file_8.close()
        self.file_16.close()
        self.file_32.close()
        self.file_64.close()
        self.file_fail.close()

    def get_writer(self, ram):
        if ram[0] == '4':
            return self.dict_writer_4
        elif ram[0] == '8':
            return self.dict_writer_8
        elif ram[:2] == '16':
            return self.dict_writer_16
        elif ram[:2] == '32':
            return self.dict_writer_32
        elif ram[:2] == '64':
            return self.dict_writer_64
        else:
            return self.dict_writer_fail


class StoreImgPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        pc_name = item['name'].lower().replace(' ', '_')
        return f'{pc_name}/{image_guid}.jpg'
