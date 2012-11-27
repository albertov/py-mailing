#coding: utf8

from ..models import Image, Session
from .. import app
from ..validators import (validate, Schema, UnicodeString, Int, String,
                          FieldStorageUploadConverter)
from .base import (rest_views, abort, request, response, generic_creator,
                   error_handler, _, ErrorResponse, error_response,
                   json_on_html, InvalidForm, invalid_form_response,
                   update_from_form)
                

class ImageValidator(Schema):
    title = UnicodeString(allow_empty=True)
    filename = UnicodeString(allow_empty=False)
    data = String(allow_empty=True)

class ShowImageValidator(Schema):
    width = Int(if_missing=None)
    height = Int(if_missing=None)

_creator = generic_creator(Image, ImageValidator)
def creator(data):
    try:
        im_data = data['data'].decode('hex')
    except TypeError:
        raise ErrorResponse('Image data must be hex-encoded')
    data['data'] = im_data
    ob = _creator(data)
    if not ob.data:
        ob.data = Image.blank_image(1, 1, 'image/png')
    if not ob.content_type or 'image' not in ob.content_type:
        raise ErrorResponse(_(u"El fichero no es una imágen válida"))
    return ob

rest_views(app, Image, '/image/', 'images',
    creator=creator,
    validator=ImageValidator)

class ImageUploadValidator(ImageValidator):
    data = FieldStorageUploadConverter(allow_empty=False)
    
    attr_name = 'data'
    filename_name = 'filename'
    coding = 'hex'
    method = 'encode'

    def _to_python(self, value, state=None):
        value = Schema._to_python(self, value, state)
        if value[self.attr_name] and hasattr(value[self.attr_name], 'file'):
            data = value[self.attr_name].file.read()
            if self.filename_name:
                value[self.filename_name] = value[self.attr_name].filename
            value[self.attr_name] = getattr(data, self.method)(self.coding)
        return super(ImageUploadValidator, self)._to_python(value, state)


@app.post("/image/upload", name='image.upload')
@error_handler
def upload():
    form = validate(ImageUploadValidator(ignore_key_missing=True),
                    request.POST, raises=False)
    if not form.is_valid:
        resp = error_response(form.message, form.errors)
    else:
        try:
            ob = creator(form)
        except ErrorResponse, e:
            resp = error_response(unicode(e), e.errors)
        except InvalidForm, e:
            resp = invalid_form_response(e.form)
        else:
            Session.add(ob);
            Session.commit()
            resp = dict(
                success=True,
                images=[ob.__json__()],
            )
    return json_on_html(resp)


@app.post("/image/<id>", name='image.update_upload')
@error_handler
def update_upload(id):
    ob = Image.query.get(id)
    if ob is None:
        abort(404)
    form = validate(ImageUploadValidator(ignore_key_missing=True),
                    request.POST, raises=False)
    if not form.is_valid:
        resp = error_response(form.message, form.errors)
    else:
        del form['filename']
        form['data'] = form['data'].decode('hex')
        update_from_form(ob, form)
        Session.commit()
        resp = dict(
            success=True,
            images=[ob.__json__()],
        )
    return json_on_html(resp)


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
