import scrapy
import re


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["tu-clausthal.de"]
    start_urls = ["http://www.tu-clausthal.de/"]

    def parse(self, response):
        links = response.xpath('//a/@href').extract()
        crawledLinks = ["http://www.tu-clausthal.de/"]
        # Pattern to check proper link
        # I only want to get the tutorial posts
        # linkPattern = re.compile(".*tu-clausthal\.de")

        ignoreLinks = [
            '/presse/',
            '/aktuell/events/',
            'dokumente.ub.tu-clausthal.de',
            'doku.tu-clausthal.de',
            'dokufarm.tu-clausthal.de',
            'liquidoffice.vw.tu-clausthal.de'
        ]

        igonoreExtensions = [
            'pdf',
            'png',
            'jpg',
            'jpeg',
            'zip',
            'exe',
            'tgz',
            'gif'
        ]

        for link in links:
            link = link.lower()
            if str(link).startswith('/'):
                link = response.urljoin(link)

            if 'hv/d5/vhb' in link \
                    and link not in crawledLinks:
                print('Page: ' + response.url + '; VHB link: ' + link)
                with open('log.txt', 'a') as f:
                    f.write(response.url + '; ' + link + '\n')

                # linkPattern.match(link) \
            elif link.count('=') < 3 \
                    and link not in crawledLinks \
                    and not any(l in link for l in ignoreLinks) \
                    and link.startswith('http') \
                    and not any(link.endswith(l) for l in igonoreExtensions):

                crawledLinks.append(link)
                yield scrapy.Request(
                    link,
                    callback=self.parse
                )
