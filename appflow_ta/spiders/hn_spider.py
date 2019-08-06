import datetime
import logging
import requests
from flask import current_app

from lxml import html

from appflow_ta import utils
from appflow_ta.models import Post, db

logging.basicConfig(format="%(asctime)s[%(levelname)s]: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger("spider")


class HackerNewsSpider:
    def __init__(self) -> None:
        self.url = r'https://news.ycombinator.com/'
        self.current_timestanp = None

    def fetch(self, session):
        with session.get(self.url) as response:
            return response.text

    def crawl(self) -> None:
        logger.info(f"Start crawl {self.url}...")
        with requests.Session() as session:
            text = self.fetch(session)

            self.current_timestanp = datetime.datetime.utcnow()
            self.parse(text)

    def parse(self, text: str) -> None:
        tree = html.fromstring(text)
        athings = tree.xpath('//tr[@class="athing"]')
        new_posts_counter = 0

        for athing in athings:
            source_id = athing.attrib['id']
            post_exists = db.session.query(Post.id).filter_by(source_id=source_id).scalar()
            if post_exists is not None:
                continue

            storylink = athing.xpath('./td[@class="title"]//a[@class="storylink"]')[0]
            url = storylink.attrib['href']
            title = storylink.text

            age = athing.xpath('(./following-sibling::tr)[1]/td/span[@class="age"]/a/text()')[0]
            created = self.current_timestanp - utils.convert_age_to_timedelta(age)

            new_posts_counter += 1
            post = Post(source_id=source_id,
                        title=title,
                        url=url,
                        created=created)
            db.session.add(post)
        db.session.commit()

        logger.info(f"...added {new_posts_counter} new posts")