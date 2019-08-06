from appflow_ta.models import Post
from appflow_ta.schemas import ma

class PostSchema(ma.ModelSchema):
    class Meta:
        model = Post
        exclude = ('source_id', )