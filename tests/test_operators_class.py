from business_rules.operators import BaseType, type_operator
from unittest2 import TestCase

class OperatorsClassTests(TestCase):
    """ Test methods on classes that inherit from BaseType.
    """

    def test_base_has_no_operators(self):
        self.assertEqual(len(BaseType.get_all_operators()), 0)

    def test_get_all_operators(self):
        """ Returns a dictionary listing all the operators on the class
        that can be called on that type, with some data about them.
        """
        class SomeType(BaseType):

            @type_operator(input_type='text')
            def some_operator(self):
                return True

            def not_an_operator(self):
                return 'yo yo'

        operators = SomeType.get_all_operators()
        self.assertEqual(len(operators), 1)
        some_operator = operators[0]
        self.assertEqual(some_operator['name'], 'some_operator')
        self.assertEqual(some_operator['description'], 'Some Operator')
        self.assertEqual(some_operator['input_type'], 'text')
