import re

class BaseType(object):
    def __init__(self, value):
        self.value = value

class StringType(BaseType):

    def __init__(self, value):
        value = value or ""
        super(StringType, self).__init__(value)

    def equal_to(self, other_string):
        return self.value == other_string

    def starts_with(self, other_string):
        return self.value.startswith(other_string)

    def ends_with(self, other_string):
        return self.value.endswith(other_string)

    def contains(self, other_string):
        return other_string in self.value

    def matches_regex(self, regex):
        return re.search(regex, self.value)

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

    def equal_to(self, other_numeric):
        return abs(self.value - self._assert_numeric_and_cast(other_numeric)) <= self.EPSILON

    def greater_than(self, other_numeric):
        return self.value > other_numeric

# def do_comparison(comparison, type_object1, type_object2):
#     def fallback(type_object2):
#         raise Exception("Comparison {0} doesnt exist for type {1}".format(comparison, type_object1.type))
#     comp_function = getattr(type_object1, comparison, fallback)
#     return comp_function(type_object2)
