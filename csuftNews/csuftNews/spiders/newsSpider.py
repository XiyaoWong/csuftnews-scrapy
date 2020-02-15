import re
import scrapy
from csuftNews.items import CsuftnewsItem


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["xww.csuft.edu.cn"]
    start_urls = [
        'http://xww.csuft.edu.cn/tzgg/',
        'http://xww.csuft.edu.cn/ldxw/',
        'http://xww.csuft.edu.cn/xsxy/',
        'http://xww.csuft.edu.cn/xydt/',
    ]

    def detail_parse(self, response):
        item = CsuftnewsItem()
        item['title'] = response.xpath("//div[@class='title']/text()").extract_first()
        item['body'] = response.xpath("//div[@class='cont']").extract_first()
        item['date'] = response.xpath("//div[@class='title_1']/text()").extract_first()
        l = response.url
        if 'tzgg' in l:
            category = 'tzgg'
        elif 'ldxw' in l:
            category = 'ldxw'
        elif 'xsxy' in l:
            category = 'xsxy'
        elif 'xydt' in l:
            category = 'xydt'
        else:
            category = 'normal'
        item['category'] = category
        yield item

    def parse(self, response):
        links = response.xpath("//div[@class='con2_t']/a/@href").extract()
        for link in links:
            detail_url = response.urljoin(link)
            yield scrapy.Request(url=detail_url, callback=self.detail_parse)

        next_page = int(re.findall(r'var currentPage = (\d{0,})', response.text)[0]) + 1
        if next_page <= 24:
            next_page_url = response.url + 'index_' + str(next_page) + '.html'
            if next_page_url:
                yield scrapy.Request(url=next_page_url, callback=self.parse)

