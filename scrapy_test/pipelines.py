# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyTestPipeline:

    def open_spider(self, spider):
        print('开始爬虫')

    def process_item(self, item, spider):
        # 保存数据
        title = item['title']
        book_name = item['book_name']
        content = item['content']
        with open(f"{book_name}.txt", 'a+', encoding='utf-8') as f:
            f.write(title + '\n' + content)
        print(title)
        return item

    def close_spider(self, spider):
        print('结束爬虫')
