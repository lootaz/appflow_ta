import unittest
from unittest.mock import MagicMock

from appflow_ta import utils
from appflow_ta.models import Post
from appflow_ta.spiders.hn_spider import HackerNewsSpider
from appflow_ta.tests.common import BaseTestCase
from appflow_ta.tests.resources.news_page_example import example


class CrawlerTests(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.spider = HackerNewsSpider()
        self.spider.fetch = MagicMock(return_value=example) # example have two news: one with id from exists_posts and another one not exists


    def test_convert_age_seconds(self):
        age = '14 seconds ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(14, delta.seconds)

        age = '1 second ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(1, delta.seconds)

    def test_convert_age_minutes(self):
        age = '14 minutes ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(14 * 60, delta.seconds)

        age = '1 minute ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(1 * 60, delta.seconds)

    def test_convert_age_hours(self):
        age = '14 hours ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(14 * 60 * 60, delta.seconds)

        age = '1 hour ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(1 * 60 * 60, delta.seconds)

    def test_convert_age_days(self):
        age = '14 days ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(14, delta.days)

        age = '1 day ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(1, delta.days)

    def test_convert_age_weeks(self):
        age = '14 weeks ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(14 * 7, delta.days)

        age = '1 week ago'
        delta = utils.convert_age_to_timedelta(age)
        self.assertEquals(1 * 7, delta.days)

    def test_spider(self):
        posts_number = Post.query.count()
        self.assertEqual(len(self.exists_posts), posts_number)

        self.spider.crawl()

        posts_number = Post.query.count()
        self.assertEqual(len(self.exists_posts) + 1, posts_number)

if __name__ == '__main__':
    unittest.main()