#coding: utf8
import json
import markupsafe

from ...models import Image, Session
from .. import app
from ..validators import (validate, Schema, UnicodeString, Int, String,
                          FieldStorageUploadConverter)
from .base import (rest_views, abort, request, response, generic_creator,
                   error_handler, _)
                

class ImageValidator(Schema):
    ignore_key_missing = True

    title = UnicodeString(allow_empty=True)
    filename = UnicodeString(allow_empty=False)
    data = String(allow_empty=True)

class ShowImageValidator(Schema):
    width = Int(if_missing=None)
    height = Int(if_missing=None)

_creator = generic_creator(Image, ImageValidator)
def creator(data):
    ob = _creator(data)
    if not ob.data:
        ob.data = Image.blank_image(1, 1, 'image/png')
    return ob

rest_views(app, Image, '/image/', 'images',
    creator=creator,
    validator=ImageValidator)

class ImageUploadValidator(Schema):
    title = UnicodeString(allow_empty=True)
    image = FieldStorageUploadConverter(allow_empty=False)

@app.post("/image/upload")
@error_handler
def upload_image():
    form = validate(ImageUploadValidator, request.POST, raises=False)
    if not form.is_valid:
        resp = dict(success=False, message=form.message, errors=form.errors)
    else:
        image = form['image']
        data, filename = image.file.read(), image.filename
        ob = creator(dict(title=form['title'], data=data, filename=filename))
        if not ob.content_type or 'image' not in ob.content_type:
            resp = dict(
                success=False,
                message=_("El fichero no es una imágen válida")
                )
        else:
            Session.add(ob);
            Session.commit()
            images = [ob.__json__()]
            resp = dict(
                success=True,
                images=[ob.__json__()],
            )
    response.content_type = 'text/html' # for extjs' iframe
    return markupsafe.escape(json.dumps(resp))


@app.get("/image/<hash>/view", name='image_view')
def view_image(hash):
    img = Image.by_hash(hash)
    if img is None:
        abort(404)
    data = None
    params = validate(ShowImageValidator, request.GET)
    if params.is_valid:
        w, h = params['width'], params['height']
        if w or h:
            w = w if w else h
            h = h if h else w
            data = img.thumbnail(w, h)
    if data is None:
        data = img.data
    response.content_type = img.content_type
    response.headers['Cache-Control'] = 'public, max-age=%d'%(3600*24*3650)
    return data
