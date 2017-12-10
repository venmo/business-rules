class Item(object):
    def __init__(self, code, name, line_number, quantity):
        self._code = code
        self._name = name
        self._line_number = line_number
        self._quantity = quantity

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def line_number(self):
        return self._line_number

    @property
    def quantity(self):
        return self._quantity


class Basket(object):
    def __init__(self, id, items):
        self._id = id
        self._items = items

    @property
    def id(self):
        return self._id

    @property
    def items(self):
        return self._items

    @property
    def product_codes(self):
        return [item.code for item in self.items]
