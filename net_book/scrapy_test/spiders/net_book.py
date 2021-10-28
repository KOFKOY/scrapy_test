import scrapy
from net_book.scrapy_test.items import ScrapyTestItem


class NetBook(scrapy.Spider):
    """
        爬取http://purepen.com 五大名著
    """
    book_dict = {}
    name = "netBook"  # 启动项目时要用到，必须唯一

    # 应该是要爬取的url
    start_urls = ['http://purepen.com']

    def parse_page_content(self, response):
        # print("地址:", response.url)
        item = ScrapyTestItem()
        item['book_name'] = self.book_dict[response.url.split('/')[-2]]
        title = response.css('p font b::text').get()
        content = response.xpath("/html/body/center/table/tr/td/pre/font/text() | /html/body/div[1]/table/tbody/tr/td/pre/font/text()").get()
        item['title'] = title if title is not None else ''
        item['content'] = content
        next_url = response.css('A::attr(href)').getall()[-1]
        yield item
        yield scrapy.Request(response.urljoin(next_url), callback=self.parse_page_content)

    def parse_content(self, response):
        # 第一页的url 开始
        dict_key = response.url.split('/')[-2]
        book_name = response.xpath("/html/body/center/table[1]/tr/td/p/font/b/text() | /html/body/table/tr/td/table/tr[1]/td/table[1]/tr/td/p/b/font/text()").get()
        if book_name is None:
            return
        else:
            self.book_dict[dict_key] = book_name
        content_url = response.css('TABLE TR TD A::attr(href)').get()
        yield scrapy.Request(response.urljoin(content_url), callback=self.parse_page_content)

    # 解析所有书的首页地址
    def parse(self, response, **kwargs):
        other_url = response.css('table tr td p a::attr(href)').getall()
        for temp_url in other_url:
            if "index.htm" in temp_url:
                print(temp_url)
                yield scrapy.Request(response.urljoin(temp_url), callback=self.parse_content)

