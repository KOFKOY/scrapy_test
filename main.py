import os
import sys

from scrapy.cmdline import execute


def run_spider(name: str):
    """
    运行指定爬虫
    """
    print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', name])


if __name__ == "__main__":
    run_spider("netBook")

