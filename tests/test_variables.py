from unittest import TestCase

from business_rules.operators import BooleanType, NumericType, SelectMultipleType, SelectType, StringType
from business_rules.utils import fn_name_to_pretty_label
from business_rules.variables import (
    boolean_rule_variable,
    numeric_rule_variable,
    rule_variable,
    select_multiple_rule_variable,
    select_rule_variable,
    string_rule_variable,
)


class RuleVariableTests(TestCase):
    """Tests for the base rule_variable decorator."""

    def test_pretty_label(self):
        self.assertEqual(fn_name_to_pretty_label('some_name_Of_a_thing'), 'Some Name Of A Thing')
        self.assertEqual(fn_name_to_pretty_label('hi'), 'Hi')

    def test_rule_variable_requires_instance_of_base_type(self):
        err_string = "a_string is not instance of BaseType in rule_variable " "field_type"
        with self.assertRaisesRegexp(AssertionError, err_string):

            @rule_variable('a_string')
            def some_test_function(self):
                pass

    def test_rule_variable_decorator_internals(self):
        """Make sure that the expected attributes are attached to a function
        by the variable decorators.
        """

        def some_test_function(self):
            pass

        wrapper = rule_variable(StringType, 'Foo Name', options=['op1', 'op2'])
        func = wrapper(some_test_function)
        self.assertTrue(func.is_rule_variable)
        self.assertEqual(func.label, 'Foo Name')
        self.assertEqual(func.field_type, StringType)
        self.assertEqual(func.options, ['op1', 'op2'])

    def test_rule_variable_works_as_decorator(self):
        @rule_variable(StringType, 'Blah')
        def some_test_function(self):
            pass

        self.assertTrue(some_test_function.is_rule_variable)

    def test_rule_variable_decorator_auto_fills_label(self):
        @rule_variable(StringType)
        def some_test_function(self):
            pass

        self.assertTrue(some_test_function.label, 'Some Test Function')

    ###
    ### rule_variable wrappers for each variable type
    ###

    def test_numeric_rule_variable(self):
        @numeric_rule_variable('My Label')
        def numeric_var():
            pass

        self.assertTrue(getattr(numeric_var, 'is_rule_variable'))
        self.assertEqual(getattr(numeric_var, 'field_type'), NumericType)
        self.assertEqual(getattr(numeric_var, 'label'), 'My Label')

    def test_numeric_rule_variable_no_parens(self):
        @numeric_rule_variable
        def numeric_var():
            pass

        self.assertTrue(getattr(numeric_var, 'is_rule_variable'))
        self.assertEqual(getattr(numeric_var, 'field_type'), NumericType)

    def test_string_rule_variable(self):
        @string_rule_variable(label='My Label')
        def string_var():
            pass

        self.assertTrue(getattr(string_var, 'is_rule_variable'))
        self.assertEqual(getattr(string_var, 'field_type'), StringType)
        self.assertEqual(getattr(string_var, 'label'), 'My Label')

    def test_string_rule_variable_no_parens(self):
        @string_rule_variable
        def string_var():
            pass

        self.assertTrue(getattr(string_var, 'is_rule_variable'))
        self.assertEqual(getattr(string_var, 'field_type'), StringType)

    def test_boolean_rule_variable(self):
        @boolean_rule_variable(label='My Label')
        def boolean_var():
            pass

        self.assertTrue(getattr(boolean_var, 'is_rule_variable'))
        self.assertEqual(getattr(boolean_var, 'field_type'), BooleanType)
        self.assertEqual(getattr(boolean_var, 'label'), 'My Label')

    def test_boolean_rule_variable_no_parens(self):
        @boolean_rule_variable
        def boolean_var():
            pass

        self.assertTrue(getattr(boolean_var, 'is_rule_variable'))
        self.assertEqual(getattr(boolean_var, 'field_type'), BooleanType)

    def test_select_rule_variable(self):

        options = {'foo': 'bar'}

        @select_rule_variable(options=options)
        def select_var():
            pass

        self.assertTrue(getattr(select_var, 'is_rule_variable'))
        self.assertEqual(getattr(select_var, 'field_type'), SelectType)
        self.assertEqual(getattr(select_var, 'options'), options)

    def test_select_multiple_rule_variable(self):

        options = {'foo': 'bar'}

        @select_multiple_rule_variable(options=options)
        def select_multiple_var():
            pass

        self.assertTrue(getattr(select_multiple_var, 'is_rule_variable'))
        self.assertEqual(getattr(select_multiple_var, 'field_type'), SelectMultipleType)
        self.assertEqual(getattr(select_multiple_var, 'options'), options)
