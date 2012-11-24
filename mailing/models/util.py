from sqlalchemy.orm import attributes, interfaces

class HexBinaryAttribute(object):

    def __init__(self, name):
        self._name = name
        self._proxy_attr = attributes.create_proxied_attribute(self)

    def __get__(self, instance, owner):
        if instance is None:
            col = getattr(owner, self._name)
            comparator = _HexBinaryComparator(col)
            return self._proxy_attr(owner, self._name, self, comparator)
        else:
            ob = getattr(instance, self._name)
            if ob is not None:
                ob = ob.encode('hex')
            return ob

    def __set__(self, instance, value):
        if value is not None:
            value = value.decode('hex')
        setattr(instance, self._name, value)

    def __delete__(self, instance):
        delattr(instance, self._name)


class _HexBinaryComparator(interfaces.PropComparator):

    def __init__(self, expression):
        self.expression = expression

    def __eq__(self, other):
        clause = self.__clause_element__()
        if other:
            try:
                other = other.decode('hex')
            except TypeError:
                return clause != clause # will always compare False
        return clause == other

    def __clause_element__(self):
        expr = self.expression
        while hasattr(expr, '__clause_element__'):
            expr = expr.__clause_element__()
        return expr

    def adapted(self, adapter):
        return self
