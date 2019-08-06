import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','sqlite:///appflow.db')

    DEBUG = False

    BUNDLE_ERRORS = True

    DEFAULT_LIMIT = 5
    MAX_LIMIT = 100

    HOST = '0.0.0.0'
    PORT = os.environ.get('PORT','8000')

    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'crawl_hackernews',
            'func': 'appflow_ta.services:run_crawler_service',
            'trigger': 'interval',
            'seconds': 300
        }
    ]


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
