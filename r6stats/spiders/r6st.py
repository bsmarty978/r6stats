import scrapy


class R6stSpider(scrapy.Spider):
    name = 'r6st'
    allowed_domains = ['r6.tracker.network']
    start_urls = ['http://r6.tracker.network/profile/pc/NaMeles_hOstAge']

    def parse(self, response):
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

        count = 0
        seasonal['overview'] = {}
        alltime['overview'] = {}
        alltime['genral'] = {}
        alltime['ranked'] = {}
        seasonal['ranked'] = {}
        alltime['unranked'] = {}
        alltime['casual'] = {}
        seasonal['casual'] = {}


        for i in o:
            p,v = para_value(i)
            if p == 'Top Operators':
                v = i.xpath(".//img/@title").getall()
            print(f"{p}:{v}")
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


        for i in dataset2[0].xpath(".//div[@class='trn-defstat']"):
            p,v = para_value(i)
            alltime['ranked'][p] = v

        for i in dataset2[1].xpath(".//div[@class='trn-defstat']"):
            p,v = para_value(i)
            alltime['unranked'][p] = v

        for i in response.xpath("//div[@class='trn-defstats trn-defstats--width5']/div"):
            p,v = para_value(i)
            alltime['casual'][p] = v          


        yield{
            'ign': ign,
            'total_matches' :total_matches,
            'alltime': alltime,
            'seasonal': seasonal
        }
