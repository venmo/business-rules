from business_rules.engine import check_condition
from business_rules.operators import StringType, NumericType
from business_rules.variables import BaseVariables, rule_variable

from unittest2 import TestCase

class SomeVariables(BaseVariables):

    @rule_variable(StringType)
    def foo(self):
        return "foo"

    @rule_variable(NumericType)
    def ten(self):
        return 10


class IntegrationTests(TestCase):
    """ Integration test, using the library like a user would.
    """
    def test_check_true_condition_happy_path(self):
        condition = {'name': 'foo',
                     'operator': 'contains',
                     'value': 'o'}
        self.assertTrue(check_condition(condition, SomeVariables()))
    
    def test_check_false_condition_happy_path(self):
        condition = {'name': 'foo',
                     'operator': 'contains',
                     'value': 'm'}
        self.assertFalse(check_condition(condition, SomeVariables()))

    def test_check_incorrect_method_name(self):
        condition = {'name': 'food',
                     'operator': 'equal_to',
                     'value': 'm'}
        err_string = 'Variable food is not defined in class SomeVariables'
        with self.assertRaisesRegexp(AssertionError, err_string):
            check_condition(condition, SomeVariables())

    def test_check_incorrect_operator_name(self):
        condition = {'name': 'foo',
                     'operator': 'equal_tooooze',
                     'value': 'foo'}
        with self.assertRaises(AssertionError):
            check_condition(condition, SomeVariables())
