import scrapy


class NetBook(scrapy.Spider):

    count = 1

    name = "netBook"  # 启动项目时要用到，必须唯一

    # 应该是要爬取的url
    start_urls = ['http://purepen.com/']

    def save_book(self, url):
        if 'index.htm' not in url:
            print("{} 不符合要求", url)
            return


    def parse(self, response, **kwargs):
        print("URL：{}", response.url)
        self.save_book(response.url)
        # 指定encoding 编码 并且 写入模式是w  不是wb 二进制
        with open(f'test_book{self.count}.html', 'w', encoding="utf-8") as f:
            f.write(response.body.decode("gbk"))
        self.count += 1
        other_url = response.css('table tr td p a::attr(href)').getall()
        if other_url is not None and len(other_url) > 0:
            for index, data in enumerate(other_url):
                yield scrapy.Request(response.urljoin(data), callback=self.parse)

        else:
            print('没找到新的url')
