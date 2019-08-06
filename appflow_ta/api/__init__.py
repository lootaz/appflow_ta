from flask_restful import Api

from appflow_ta.api.post_resource import PostResource

api = Api()

api.add_resource(PostResource, '/posts')