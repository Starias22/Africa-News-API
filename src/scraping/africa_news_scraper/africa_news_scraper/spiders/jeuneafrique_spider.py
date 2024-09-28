import scrapy


class JeuneafriqueSpiderSpider(scrapy.Spider):
    name = "jeuneafrique_spider"
    allowed_domains = ["jeuneafrique.com"]
    start_urls = ["https://jeuneafrique.com"]

    def parse(self, response):
        pass
