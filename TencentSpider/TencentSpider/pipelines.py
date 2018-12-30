# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import TencentSpider.items

class TencentPipeline(object):
    def __init__(self):
        self.filename = open("tencent.json", "w")
        self.linkfile = open("linkInfo.json", "w")

    def process_item(self, item, spider):
        if isinstance(item, TencentSpider.items.TencentItem):
            text = json.dumps(dict(item), ensure_ascii = False) + ",\n"
            self.filename.write(text)
            return item
        elif isinstance(item, TencentSpider.items.PagerankItem):
            text = json.dumps(dict(item), ensure_ascii = False) + ",\n"
            self.linkfile.write(text)
            return item

    def close_spider(self, spider):
        self.filename.close()
