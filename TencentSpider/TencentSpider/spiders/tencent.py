#!/usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy
# 导入CrawlSpider类和Rule
from scrapy.spiders import CrawlSpider, Rule
# 导入链接规则匹配类，用来提取符合规则的连接
from scrapy.linkextractors import LinkExtractor
from TencentSpider.items import *
import jieba.analyse


class TencentSpider(CrawlSpider):

    name = "tencent"
    allow_domains = ["hr.tencent.com"]
    start_urls = ["https://hr.tencent.com/position.php?keywords=java&lid=0&tid=0"]

    linkList = []
    seedList = []

    # Response里链接的提取规则，返回的符合匹配规则的链接匹配对象的列表
    pagelink = LinkExtractor(allow=("start=\d+"))
    pageranklink= LinkExtractor(allow = ("position_detail+"))

    rules = [
        # 获取这个列表里的链接，依次发送请求，并且继续跟进，调用指定回调函数处理
        Rule(pagelink, callback = "parseTencent", follow = True),
        Rule(pageranklink, callback= "getlinks", follow = True )
    ]

    def getlinks(self, response):
        item = PagerankItem()
        item['url'] = response.url
        item['pagelink'] = []
        for each in response.xpath("//@href"):
            item['pagelink'].append(each.extract())
        yield item


    # 指定的回调函数
    def parseTencent(self, response):
        #evenlist = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        #oddlist = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        #fulllist = evenlist + oddlist
        #for each in fulllist:
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentItem()
            # 职位名称
            name = each.xpath("./td[1]/a/text()").extract()[0];
            # 新的种子集合
            newSeedList = jieba.analyse.extract_tags(name);
            item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 详情连接
            link = each.xpath("./td[1]/a/@href").extract()[0]
            if link.find("&") >= 0:
                position = link.find("&")
                link = link[0: position]
            item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

            if link not in self.linkList:
                self.linkList.append(link)   # 若相应的item没有被记录，则记录
                yield item

            for eachSeed in newSeedList:
                if eachSeed not in self.seedList:
                    self.seedList.append(eachSeed)
                    yield scrapy.Request("https://hr.tencent.com/position.php?keywords=" + eachSeed)