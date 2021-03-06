import scrapy
import json
import codecs
import re

class QuotesSpider(scrapy.Spider):
    name = "sp"

    def start_requests(self):
        with codecs.open("urls.jl",'r','utf-8') as f:
            urls = f.readlines()
        for url in urls:
            url = re.sub(r"\n| |\r|\"", r"", url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        filename = re.sub(r"\/|:", r"_", response.url)
        with open("./news/%s" %filename , 'wb') as f:
            f.write(response.body)
#farkli filelara url ismi file ismi olcak sekilde indir
