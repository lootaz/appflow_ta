from flask import current_app
from flask_restful import Resource, reqparse
from sqlalchemy import text

from appflow_ta.models import Post
from appflow_ta.schemas.post_schema import PostSchema

def limit_type(value, name):
    MIN_VALUE = 1
    MAX_VALUE = current_app.config['MAX_LIMIT']
    ERROR_MESSAGE = f"Wrong value '{value}' for {name} parameter ({MIN_VALUE} < {name} < {MAX_VALUE})"

    try:
        value = int(value)
        if value < MIN_VALUE or value > MAX_VALUE:
            raise ValueError(ERROR_MESSAGE)
    except ValueError:
        raise ValueError(ERROR_MESSAGE)

    return value


def offset_type(value, name):
    MIN_VALUE = 0
    ERROR_MESSAGE = f"Wrong value '{value}' for {name} parameter ({MIN_VALUE} <= {name})"

    try:
        value = int(value)
        if value < MIN_VALUE:
            raise ValueError(ERROR_MESSAGE)
    except ValueError:
        raise ValueError(ERROR_MESSAGE)

    return value

class PostResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('order',
                        choices=Post.get_sort_field_names(),
                        help='Bad choice: {error_msg}')
    parser.add_argument('direct',
                        choices=('asc', 'desc'),
                        help='Bad choice: {error_msg}')
    parser.add_argument('limit',
                        type=limit_type)
    parser.add_argument('offset',
                        type=offset_type)


    def get(self):
        args = self.parser.parse_args()

        order = args.get('order')
        limit = args.get('limit') or current_app.config.get('DEFAULT_LIMIT')
        offset = args.get('offset') or 0
        direct = args.get('direct') or 'asc'

        query = Post.query
        if not order is None:
            query = query.order_by(text(f"{order} {direct}"))

        query = query.offset(offset).limit(limit)

        posts = query.all()
        schema = PostSchema()

        return schema.dump(posts, many=True)