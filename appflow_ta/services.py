from appflow_ta.models import db
from appflow_ta.spiders.hn_spider import HackerNewsSpider


def run_crawler_service():
    with db.app.app_context():
        spider = HackerNewsSpider()
        spider.crawl()
