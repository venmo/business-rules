import inspect
import re

from .utils import fn_name_to_pretty_description


TYPE_TEXT = 'text'
TYPE_NUMERIC = 'numeric'
TYPE_NO_INPUT = None

class BaseType(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def get_all_operators(cls):
        methods = inspect.getmembers(cls, predicate=inspect.ismethod)
        return [{'name': m[0],
                 'description': m[1].description,
                 'input_type': m[1].input_type
                } for m in methods if getattr(m[1], 'is_operator', False)]

def type_operator(input_type, description=None):
    """ Decorator to make a function into a type operator.
    """
    def wrapper(func):
        func.is_operator = True
        func.description = description \
                or fn_name_to_pretty_description(func.__name__)
        func.input_type = input_type
        return func
    return wrapper

class StringType(BaseType):

    def __init__(self, value):
        value = value or ""
        super(StringType, self).__init__(value)

    @type_operator(TYPE_TEXT)
    def equal_to(self, other_string):
        return self.value == other_string

    @type_operator(TYPE_TEXT, description="Equal To (case insensitive)")
    def equal_to_case_insensitive(self, other_string):
        return self.value.lower() == other_string.lower()

    @type_operator(TYPE_TEXT)
    def starts_with(self, other_string):
        return self.value.startswith(other_string)

    @type_operator(TYPE_TEXT)
    def ends_with(self, other_string):
        return self.value.endswith(other_string)

    @type_operator(TYPE_TEXT)
    def contains(self, other_string):
        return other_string in self.value

    @type_operator(TYPE_TEXT)
    def matches_regex(self, regex):
        return re.search(regex, self.value)

    @type_operator(TYPE_NO_INPUT)
    def non_empty(self):
        return bool(self.value)

class NumericType(BaseType):
    EPSILON = 0.000001

    def __init__(self, value):
        value = self._assert_numeric_and_cast(value)
        super(NumericType, self).__init__(value)

    @staticmethod
    def _assert_numeric_and_cast(value):
        if not isinstance(value, (float, int)):
            raise Exception("{0} is not a valid numeric type.".format(value))
        return float(value)

    @type_operator(TYPE_NUMERIC)
    def equal_to(self, other_numeric):
        return abs(self.value - self._assert_numeric_and_cast(other_numeric)) <= self.EPSILON

    @type_operator(TYPE_NUMERIC)
    def greater_than(self, other_numeric):
        return self.value > other_numeric
