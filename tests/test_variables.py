from . import TestCase
from business_rules.utils import fn_name_to_pretty_label
from business_rules.variables import (rule_variable,
                                      numeric_rule_variable,
                                      string_rule_variable,
                                      boolean_rule_variable,
                                      select_rule_variable,
                                      select_multiple_rule_variable,
                                      TYPE_STRING,
                                      TYPE_NUMERIC,
                                      TYPE_BOOLEAN,
                                      TYPE_SELECT,
                                      TYPE_SELECT_MULTIPLE)

class RuleVariableTests(TestCase):
    """ Tests for the base rule_variable decorator.
    """

    def test_pretty_label(self):
        self.assertEqual(
                fn_name_to_pretty_label('some_name_Of_a_thing'),
                'Some Name Of A Thing')
        self.assertEqual(fn_name_to_pretty_label('hi'), 'Hi')

    def test_rule_variable_decorator_internals(self):
        """ Make sure that the expected attributes are attached to a function
        by the variable decorators.
        """
        def some_test_function(self): pass
        wrapper = rule_variable(TYPE_STRING, 'Foo Name', options=['op1', 'op2'])
        func = wrapper(some_test_function)
        self.assertTrue(func.is_rule_variable)
        self.assertEqual(func.label, 'Foo Name')
        self.assertEqual(func.field_type, TYPE_STRING)
        self.assertEqual(func.options, ['op1', 'op2'])

    def test_rule_variable_works_as_decorator(self):
        @rule_variable(TYPE_STRING, 'Blah')
        def some_test_function(self): pass
        self.assertTrue(some_test_function.is_rule_variable)

    def test_rule_variable_decorator_auto_fills_label(self):
        @rule_variable(TYPE_STRING)
        def some_test_function(self): pass
        self.assertTrue(some_test_function.label, 'Some Test Function')

    def test_rule_variable_decorator_caches_value(self):
        foo = 1
        @rule_variable(TYPE_NUMERIC)
        def foo_func():
            return foo
        self.assertEqual(foo_func(), 1)
        foo = 2
        self.assertEqual(foo_func(), 1)

    def test_rule_variable_decorator_doesnt_cache_value_with_option_passed(self):
        foo = 1
        @rule_variable(TYPE_NUMERIC, cache_result=False)
        def foo_func():
            return foo
        self.assertEqual(foo_func(), 1)
        foo = 2
        self.assertEqual(foo_func(), 2)
    
    ###
    ### rule_variable wrappers for each variable type
    ###

    def test_numeric_rule_variable(self):

        @numeric_rule_variable()
        def numeric_var(): pass
        
        self.assertTrue(getattr(numeric_var, 'is_rule_variable'))
        self.assertEqual(getattr(numeric_var, 'field_type'), TYPE_NUMERIC)

    def test_string_rule_variable(self):

        @string_rule_variable()
        def string_var(): pass
        
        self.assertTrue(getattr(string_var, 'is_rule_variable'))
        self.assertEqual(getattr(string_var, 'field_type'), TYPE_STRING)
    
    def test_boolean_rule_variable(self):

        @boolean_rule_variable()
        def boolean_var(): pass
        
        self.assertTrue(getattr(boolean_var, 'is_rule_variable'))
        self.assertEqual(getattr(boolean_var, 'field_type'), TYPE_BOOLEAN)

    def test_select_rule_variable(self):

        options = {'foo':'bar'}
        @select_rule_variable(options=options)
        def select_var(): pass
        
        self.assertTrue(getattr(select_var, 'is_rule_variable'))
        self.assertEqual(getattr(select_var, 'field_type'), TYPE_SELECT)
        self.assertEqual(getattr(select_var, 'options'), options)

    def test_select_multiple_rule_variable(self):

        options = {'foo':'bar'}
        @select_multiple_rule_variable(options=options)
        def select_multiple_var(): pass
        
        self.assertTrue(getattr(select_multiple_var, 'is_rule_variable'))
        self.assertEqual(getattr(select_multiple_var, 'field_type'), TYPE_SELECT_MULTIPLE)
        self.assertEqual(getattr(select_multiple_var, 'options'), options)
