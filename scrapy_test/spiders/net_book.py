import scrapy
from scrapy_test.items import ScrapyTestItem


class NetBook(scrapy.Spider):
    """
        爬取http://purepen.com 五大名著
    """
    book_dict = {}
    name = "netBook"  # 启动项目时要用到，必须唯一

    # 应该是要爬取的url
    start_urls = ['http://purepen.com']

    def parse_page_content(self, response):
        print("地址:", response.url)
        item = response.meta['item']
        next_url = response.css('A::attr(href)').getall()[-1]
        title = response.css('p font b::text').get()
        content = response.css('center table tr td pre font::text').get()
        item['title'] = title
        item['content'] = content
        yield item
        yield scrapy.Request(response.urljoin(next_url), callback=self.parse_page_content)

    def parse_content(self, response):
        # 第一页的url 开始
        dict_key = response.url.split('/')[-2]
        book_name = response.css('center table tr td p font b::text').get()
        if book_name is None:
            if dict_key in self.book_dict.keys():
                book_name = self.book_dict[dict_key]
            else:
                return
        else:
            self.book_dict[dict_key] = book_name
        item = ScrapyTestItem()
        item['book_name'] = book_name
        content_url = response.css('TABLE TR TD A::attr(href)').get()
        if content_url == 'http://purepen.com/sgyy/002.htm':
            print("cccc")
        print(item)
        yield scrapy.Request(response.urljoin(content_url), callback=self.parse_page_content, meta={'item': item})

    # 解析所有书的首页地址
    def parse(self, response, **kwargs):
        print("URL：{}", response.url)
        other_url = response.css('table tr td p a::attr(href)').getall()
        for temp_url in other_url:
            if "index.htm" in temp_url:
                yield scrapy.Request(response.urljoin(temp_url), callback=self.parse_content)

