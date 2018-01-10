import scrapy
import re
import codecs
import json

class QuotesSpider(scrapy.Spider):
    name = "urlspider"
    days = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
    months = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    years = ["1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"]
    d = 0
    m = 4
    y = 0
    def start_requests(self):
        urls = [
            'http://archive.indianexpress.com/archive/news/1/5/1997/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
#        urls = response.xpath('//table[@class="cnt"][last()]//tr[last()]/td[@width="670"]/div[last()]//a/@href').extract()
        print(response.url)
        urlfilename = re.sub(r"\/|:", r"_", response.url)
        with open("./urlhtmls/%s" %urlfilename, 'wb') as g:
            g.write(response.body)
        urls = response.xpath('//div[@id="box_left"]//a/@href').extract()
        filename = 'urls.jl'
        with codecs.open(filename, 'a', 'utf-8') as f:
            for rl in urls:
                line = json.dumps(rl,ensure_ascii=False) + "\n"
                f.write(line)
        if(self.months[self.m] == "1" or self.months[self.m] == "3" or self.months[self.m] == "5" or self.months[self.m] == "7" or self.months[self.m] == "8" or self.months[self.m] == "10"):
            if(self.days[self.d] == "31"):
                self.m = self.m + 1
                self.d = 0
            else:
                self.d = self.d + 1
        elif(self.months[self.m] == "12"):
            if(self.days[self.d] == "31"):
                self.y = self.y + 1
                self.m = 0
                self.d = 0
            else:
                self.d = self.d + 1
        elif(self.months[self.m] == "4" or self.months[self.m] == "6" or self.months[self.m] == "9" or self.months[self.m] == "11"):
            if(self.days[self.d] == "30"):
                self.m = self.m + 1
                self.d = 0
            else:
                self.d = self.d + 1
        else:
            intyear = int(self.years[self.y])
            if(intyear % 4 == 0):
                if(self.days[self.d] == "29"):
                    self.m = self.m + 1
                    self.d = 0
                else:
                    self.d = self.d + 1
            else:
                if(self.days[self.d] == "28"):
                    self.m = self.m + 1
                    self.d = 0
                else:
                    self.d = self.d + 1
        if(self.years[self.y] == "2014" and self.months[self.m] == "1" and self.days[self.d] == "16"):
            print("Finished")
        else:
            url = "http://archive.indianexpress.com/archive/news/" + self.days[self.d] + "/" + self.months[self.m] + "/" + self.years[self.y] + "/"
            yield scrapy.Request(url, callback=self.parse)
