import scrapy
from scrapy import signals


class StudiumSpider(scrapy.Spider):
    name = "studium"
    allowed_domains = ["studium.tu-clausthal.de"]
    start_urls = ["https://www.studium.tu-clausthal.de/"]

    crawled_links = ["https://www.studium.tu-clausthal.de/"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StudiumSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse(self, response):
        self.crawled_links.append(response.url)
        links = response.xpath('//a/@href').extract()

        ignore_extensions = [
            'pdf',
            'png',
            'jpg',
            'jpeg',
            'zip',
            'exe',
            'tgz',
            'gif'
        ]

        ignore_url_content = [
            '?'
        ]

        for link in links:
            link = link.lower()
            if not link.startswith('http'):
                link = response.urljoin(link)

            if link not in self.crawled_links \
                    and link.startswith('http') \
                    and not any(link.endswith(l) for l in ignore_extensions) \
                    and not any(l in link for l in ignore_url_content):

                yield scrapy.Request(
                    link,
                    callback=self.parse
                )

    def spider_closed(self, spider):
        for l in self.crawled_links:
            with open('studiumLog.txt', 'a') as f:
                f.write(l + '\n')