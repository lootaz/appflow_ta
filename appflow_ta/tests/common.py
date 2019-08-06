import datetime
import unittest

from appflow_ta.config import TestConfig
from appflow_ta.models import db, Post
from manage import app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.client = app.test_client()
        db.drop_all()
        db.create_all()

        now = datetime.datetime.utcnow()
        self.exists_posts = [
            Post(source_id=111, title="Test_444", url="http://test.org/666", created=now),
            Post(source_id=222, title="Test_333", url="http://test.org/333", created=now),
            Post(source_id=333, title="Test_222", url="http://test.org/444", created=now),
            Post(source_id=444, title="Test_111", url="http://test.org/222", created=now),
            Post(source_id=555, title="Test_555", url="http://test.org/111", created=now),
            Post(source_id=666, title="Test_666", url="http://test.org/555", created=now),
        ]
        db.session.add_all(self.exists_posts)
        db.session.commit()


    def tearDown(self):
        pass
