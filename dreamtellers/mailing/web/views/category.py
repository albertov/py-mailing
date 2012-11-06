from ...models import Category

from .. import app
from ..validators import Schema, Int, UnicodeString
from .base import rest_views

class CategoryValidator(Schema):
    category_id = Int(min=0, if_missing=None)
    title = UnicodeString(allow_empty=False)

rest_views(app, Category, '/category/', 'categories',
           validator=CategoryValidator,
           collection_query=Category.category_id==None)
