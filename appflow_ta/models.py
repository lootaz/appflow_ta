from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={
    'expire_on_commit': False
})

class Post(db.Model):
    __tablename__ = 'af_post'

    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def get_sort_field_names():
        return ('id', 'title', 'url', 'created')