import scrapy
from scrapy.exceptions import CloseSpider

class R6stSpider(scrapy.Spider):
    name = 'r6st'
    allowed_domains = ['r6.tracker.network']
    # start_urls = [f'http://r6.tracker.network/profile/pc/{player}']
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url=f'http://r6.tracker.network/profile/{self.pl}/{self.p}', headers={
            'User-Agent': self.user_agent
        })

    def parse(self, response):

        if response.status == 404:
            print(">>>>>>>>>>>>>>>>>>>>>>>>404")
            yield {
                "ign" : "not found"
            }
            CloseSpider('Ign not found')

        def para_value(dataobject):
            p = dataobject.xpath("normalize-space(.//div[@class='trn-defstat__name']/text())").get()
            v = dataobject.xpath("normalize-space(.//div[@class='trn-defstat__value']/text())").get()
            return p,v

        ign = response.xpath("normalize-space(//h1[@class='trn-profile-header__name']/span[1]/text())").get()
        total_matches = response.xpath("//div[@class='trn-card__header-subline']/text()").get()
        seasonal = {}
        alltime = {}

        season_name = response.xpath("(//h2[@class='trn-card__header-title'])[5]/text()").get()
        season_total_matches =  response.xpath("normalize-space(//span[@class='trn-card__header-subline']/text())").get()
        seasonal['name'] = season_name
        seasonal['total matches'] = season_total_matches

        o = response.xpath("//div[@class='trn-card__content trn-card--light trn-defstats-grid']/div")
        datasets = response.xpath("//div[@class='trn-defstats trn-defstats--width4']")
        dataset2 = response.xpath("//div[@class='trn-defstats ']")

      
        seasonal['overview'] = {}
        alltime['overview'] = {}
        alltime['genral'] = {}
        alltime['ranked'] = {}
        seasonal['ranked'] = {}
        alltime['unranked'] = {}
        alltime['casual'] = {}
        seasonal['casual'] = {}

        count = 0
        for i in o:
            p,v = para_value(i)
            if p == 'Top Operators':
                v = i.xpath(".//img/@title").getall()
            # print(f"{p}:{v}")
            if count <= 4:
                alltime['overview'][p] = v
            else:
                seasonal['overview'][p] = v
            count += 1

        for i in datasets[0].xpath(".//div[@class='trn-defstat trn-defstat--large']"):
            p,v = para_value(i)
            alltime['overview'][p] = v
        
        for i in datasets[1].xpath(".//div[@class='trn-defstat trn-defstat--large']"):
            p,v = para_value(i)
            seasonal['overview'][p] = v

        for i in datasets[2].xpath(".//div[@class='trn-defstat']"):
            p,v = para_value(i)
            alltime['genral'][p] = v

        for i in datasets[3].xpath(".//div[@class='trn-defstat']"):
            p,v = para_value(i)
            seasonal['ranked'][p] = v

        for i in datasets[4].xpath(".//div[@class='trn-defstat']"):
            p,v = para_value(i)
            seasonal['casual'][p] = v

        count_ds2 = 0
        for dataset in dataset2:
            for i in dataset.xpath(".//div[@class='trn-defstat']"):
                p,v = para_value(i)
                if count_ds2 == 0:
                    alltime['ranked'][p] = v
                else:
                    alltime['unranked'][p] = v
            count_ds2 += 1

        for i in response.xpath("//div[@class='trn-defstats trn-defstats--width5']/div"):
            p,v = para_value(i)
            alltime['casual'][p] = v 

        alias = []
        for i in response.xpath("//table[@class='trn-table']/tbody/tr/td[1]/text()").getall():
            alias.append(i.strip())

        yield{
            'ign': ign,
            'alias' : alias,
            'photo' : response.xpath("//div[@class='trn-profile-header trn-card']//img/@src").get(),
            'total_matches' :total_matches,
            'alltime': alltime,
            'seasonal': seasonal,
            'url' : response.url
        }
