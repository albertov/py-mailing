from sqlalchemy.ext.hybrid import hybrid_property, Comparator

class HexBinaryComparator(Comparator):
    def __eq__(self, other):
        clause = self.__clause_element__()
        if other:
            try:
                other = other.decode('hex')
            except TypeError:
                return clause != clause # will always compare False
        return clause == other
