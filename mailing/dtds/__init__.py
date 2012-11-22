from lxml import etree
from pkg_resources import resource_filename

class DTDResolver(etree.Resolver):
    def resolve(self, url, id, context):
        basename = url.split('/')[-1]
        filename = resource_filename(__name__, basename)
        return self.resolve_filename(filename, context)
