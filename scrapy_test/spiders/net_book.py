import scrapy
from scrapy_test.items import ScrapyTestItem


class NetBook(scrapy.Spider):
    """
        爬取http://purepen.com 五大名著
    """
    count = 1
    book_dict = {}
    name = "netBook"  # 启动项目时要用到，必须唯一

    # 应该是要爬取的url
    start_urls = ['http://purepen.com']

    # start_urls = ['http://purepen.com/sgyy/index.htm']

    def parse(self, response, **kwargs):
        print("URL：{}", response.url)
        url = response.url

        if url in self.start_urls:
            other_url = response.css('table tr td p a::attr(href)').getall()
            for temp_url in other_url:
                if "index.htm" in temp_url:
                    yield scrapy.Request(response.urljoin(temp_url), callback=self.parse)
        else:
            dict_key = url.split('/')[-2]
            book_name = response.css('center table tr td p font b::text').get()
            if book_name is None:
                if dict_key in self.book_dict.keys():
                    book_name = self.book_dict[dict_key]
                else:
                    book_name = 'unknown'
            else:
                self.book_dict[dict_key] = book_name
            content_url = response.css('TABLE TR TD A::attr(href)').get()
            title = response.css('p font b::text').get()
            if title is not None:
                content = response.css('center table tr td pre font::text').get()
                if content is not None:
                    item = ScrapyTestItem()
                    item['book_name'] = book_name
                    item['title'] = title
                    item['content'] = content
                    yield item
            if content_url is None:
                # 取第一页
                content_url = response.css('A::attr(href)').getall()[-1]
            if content_url is not None:
                yield scrapy.Request(response.urljoin(content_url), callback=self.parse)
