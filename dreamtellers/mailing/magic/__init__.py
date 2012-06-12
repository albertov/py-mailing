from glob import glob

from pkg_resources import resource_filename

from .magic import Magic

def from_buffer(fileobj, type='mime'):
    return _magics[type].classify(fileobj)

_magics = dict((fname.split('.')[-1], Magic(fname))
               for fname in glob(resource_filename(__name__, 'magic.*'))
               if not fname.split('.')[-1].startswith('py'))

