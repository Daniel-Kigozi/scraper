import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater

class VehicleSpider(scrapy.Spider):
    name ="vehicles"
    start_urls = [
        'https://www.harbourviewvw.com/en/new'
    ]

    def parse(self, response):
        for vehicle in response.css('div.catalog-block__wrapper'):
            yield {
                'make': vehicle.css('div.catalog-block__wrapper::attr(data-make)').getall(),
                'model': vehicle.css('div.catalog-block__wrapper::attr(data-model)').getall(),
                'year': vehicle.css('div.catalog-block__wrapper::attr(data-year)').getall(),
                'body_style': vehicle.css('div.catalog-block__wrapper::attr(data-bodystyle)').getall(),
                'price': vehicle.css('div.catalog-block__wrapper::attr(data-price)').getall(),
                'id': vehicle.css('div.catalog-block__wrapper::attr(data-id)').getall(),
                
            }

def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)

process = CrawlerProcess(get_project_settings())


def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print('waiting 30 seconds before restart...'))
    deferred.addCallback(sleep, seconds=30)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, VehicleSpider)
process.start()
