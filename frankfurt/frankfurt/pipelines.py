# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class FrankfurtPipeline:
    def process_item(self, item, spider):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(",\n\t")
        product = json.dumps(dict(item), indent=4)
        self.file.write(product)
        return item

    def open_spider(self, spider):
        self.file = open("products.json", "w")
        self.file.write("[\n\t")
        self.first_item = True
    
    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()