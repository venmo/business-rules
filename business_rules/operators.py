import re

class BaseType(object):
    def __init__(self, value):
        self.value = value

class StringType(BaseType):

    def __init__(self, value):
        value = value or ""
        super(StringType, self).__init__(value)

    def equals(self, other_string):
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

# def do_comparison(comparison, type_object1, type_object2):
#     def fallback(type_object2):
#         raise Exception("Comparison {0} doesnt exist for type {1}".format(comparison, type_object1.type))
#     comp_function = getattr(type_object1, comparison, fallback)
#     return comp_function(type_object2)
