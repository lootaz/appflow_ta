import datetime
import unittest

from sqlalchemy import asc, desc

from appflow_ta.config import TestConfig
from appflow_ta.models import db, Post
from appflow_ta.tests.common import BaseTestCase
from manage import app


class ApiTests(BaseTestCase):
    def test_get_posts(self):
        response = self.client.get('/posts')
        self.assertEqual(200, response.status_code)

    def test_limit(self):
        response = self.client.get('/posts?limit=1')
        self.assertEqual(1, len(response.json))

    def test_limit_default(self):
        response = self.client.get('/posts')
        self.assertEqual(app.config['DEFAULT_LIMIT'], len(response.json))

    def test_limit_too_low(self):
        response = self.client.get(f'/posts?limit=0')
        self.assertEqual(400, response.status_code)

    def test_limit_too_high(self):
        response = self.client.get(f'/posts?limit={app.config["MAX_LIMIT"] + 1}')
        self.assertEqual(400, response.status_code)

    def test_negative_limit(self):
        response = self.client.get(f'/posts?limit=-100')
        self.assertEqual(400, response.status_code)

    def test_order_by_id_asc(self):
        response = self.client.get(f'/posts?order=id')
        self.assertEqual(min(post.id for post in self.exists_posts), response.json[0].get('id'))

        response = self.client.get(f'/posts?order=id&direct=asc')
        self.assertEqual(min(post.id for post in self.exists_posts), response.json[0].get('id'))

    def test_order_by_id_desc(self):
        response = self.client.get(f'/posts?order=id&direct=desc')
        self.assertEqual(max(post.id for post in self.exists_posts), response.json[0].get('id'))

    def test_order_by_title_asc(self):
        post = Post.query.order_by(asc('title')).first()

        response = self.client.get(f'/posts?order=title')
        self.assertEqual(post.id, response.json[0].get('id'))

        response = self.client.get(f'/posts?order=title&direct=asc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_title_desc(self):
        post = Post.query.order_by(desc('title')).first()

        response = self.client.get(f'/posts?order=title&direct=desc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_url_asc(self):
        post = Post.query.order_by(asc('url')).first()

        response = self.client.get(f'/posts?order=url')
        self.assertEqual(post.id, response.json[0].get('id'))

        response = self.client.get(f'/posts?order=url&direct=asc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_url_desc(self):
        post = Post.query.order_by(desc('url')).first()

        response = self.client.get(f'/posts?order=url&direct=desc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_created_asc(self):
        post = Post.query.order_by(asc('created')).first()

        response = self.client.get(f'/posts?order=created')

        self.assertEqual(post.id, response.json[0].get('id'))

        response = self.client.get(f'/posts?order=created&direct=asc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_created_desc(self):
        post = Post.query.order_by(desc('created')).first()

        response = self.client.get(f'/posts?order=created&direct=desc')
        self.assertEqual(post.id, response.json[0].get('id'))

    def test_order_by_wrong_field(self):
        response = self.client.get(f'/posts?order=id2')
        self.assertEqual(400, response.status_code)

    def test_offset(self):
        response = self.client.get(f'/posts?offset=1')
        self.assertEqual(min(post.id for post in self.exists_posts) + 1, response.json[0].get('id'))



if __name__ == '__main__':
    unittest.main()