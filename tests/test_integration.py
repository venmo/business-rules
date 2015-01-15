from business_rules.engine import check_condition
from business_rules import export_rule_data
from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable, date_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT

from . import TestCase

class SomeVariables(BaseVariables):

    @string_rule_variable()
    def foo(self):
        return "foo"

    @numeric_rule_variable(params=[{'field_type': FIELD_NUMERIC, 'name': 'x', 'label': 'X'}])
    def x_plus_one(self, x):
        return x + 1

    @numeric_rule_variable(label="Diez")
    def ten(self):
        return 10

    @date_rule_variable(label="MyDate")
    def january_one_2015(self):
        return '01/01/2015'

    @boolean_rule_variable()
    def true_bool(self):
        return True

class SomeActions(BaseActions):

    @rule_action(params={"foo": FIELD_NUMERIC})
    def some_action(self, foo): pass

    @rule_action(label="woohoo", params={"bar": FIELD_TEXT})
    def some_other_action(self, bar): pass

    @rule_action(params=[{'fieldType': FIELD_SELECT,
                          'name': 'baz',
                          'label': 'Baz',
                          'options': [
                            {'label': 'Chose Me', 'name': 'chose_me'},
                            {'label': 'Or Me', 'name': 'or_me'}
                        ]}])
    def some_select_action(self, baz): pass


class IntegrationTests(TestCase):
    """ Integration test, using the library like a user would.
    """
    def test_true_boolean_variable(self):
        condition = {
            'name': 'true_bool',
            'operator': 'is_true',
            'value': ''
        }
        res = check_condition(condition, SomeVariables())
        self.assertTrue(res)

    def test_false_boolean_variable(self):
        condition = {
            'name': 'true_bool',
            'operator': 'is_false',
            'value': ''
        }
        res = check_condition(condition, SomeVariables())
        self.assertFalse(res)

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

    def test_numeric_variable_with_params(self):
        condition = {'name': 'x_plus_one',
                     'operator': 'equal_to',
                     'value': 10,
                     'params': {'x': 9}}
        self.assertTrue(check_condition(condition, SomeVariables()))

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


    def test_export_rule_data(self):
        """ Tests that export_rule_data has the three expected keys
        in the right format.
        """
        all_data = export_rule_data(SomeVariables(), SomeActions())
        self.assertEqual(all_data.get("actions"),
                [{"name": "some_action",
                  "label": "Some Action",
                  "params": [{'fieldType': 'numeric', 'label': 'Foo', 'name': 'foo'}]},
                 {"name": "some_other_action",
                  "label": "woohoo",
                  "params": [{'fieldType': 'text', 'label': 'Bar', 'name': 'bar'}]},
                 {"name": "some_select_action",
                  "label": "Some Select Action",
                  "params":[{'fieldType': FIELD_SELECT,
                             'name': 'baz',
                             'label': 'Baz',
                             'options': [
                                {'label': 'Chose Me', 'name': 'chose_me'},
                                {'label': 'Or Me', 'name': 'or_me'}
                            ]}]
                  }
                 ])

        self.assertEqual(all_data.get("variables"),
                         [{'field_type': 'string',
                           'label': 'Foo',
                           'name': 'foo',
                           'options': [],
                           'params': []},
                          {'field_type': 'date',
                           'label': 'MyDate',
                           'name': 'january_one_2015',
                           'options': [],
                           'params': []},
                          {'field_type': 'numeric',
                           'label': 'Diez',
                           'name': 'ten',
                           'options': [],
                           'params': []},
                          {'field_type': 'boolean',
                           'label': 'True Bool',
                           'name': 'true_bool',
                           'options': [],
                           'params': []},
                          {'field_type': 'numeric',
                           'label': 'X Plus One',
                           'name': 'x_plus_one',
                           'options': [],
                           'params': [{'field_type': 'numeric', 'label': 'X', 'name': 'x'}]}]
                         )

        self.assertEqual(all_data.get("variable_type_operators"),
                         {'boolean': [{'input_type': 'none',
                             'label': 'Is False',
                             'name': 'is_false'},
                            {'input_type': 'none',
                             'label': 'Is True',
                             'name': 'is_true'}],
                           'date': [{'input_type': 'date',
                             'label': 'Equal To',
                             'name': 'equal_to'},
                            {'input_type': 'date',
                             'label': 'Greater Than',
                             'name': 'greater_than'},
                            {'input_type': 'date',
                             'label': 'Greater Than Or Equal To',
                             'name': 'greater_than_or_equal_to'},
                            {'input_type': 'date',
                             'label': 'Less Than',
                             'name': 'less_than'},
                            {'input_type': 'date',
                             'label': 'Less Than Or Equal To',
                             'name': 'less_than_or_equal_to'}],
                           'numeric': [{'input_type': 'numeric',
                             'label': 'Equal To',
                             'name': 'equal_to'},
                            {'input_type': 'numeric', 'label': 'Greater Than', 'name': 'greater_than'},
                            {'input_type': 'numeric',
                             'label': 'Greater Than Or Equal To',
                             'name': 'greater_than_or_equal_to'},
                            {'input_type': 'numeric', 'label': 'Less Than', 'name': 'less_than'},
                            {'input_type': 'numeric',
                             'label': 'Less Than Or Equal To',
                             'name': 'less_than_or_equal_to'}],
                           'select': [{'input_type': 'select', 'label': 'Contains', 'name': 'contains'},
                            {'input_type': 'select',
                             'label': 'Does Not Contain',
                             'name': 'does_not_contain'}],
                           'select_multiple': [{'input_type': 'select_multiple',
                             'label': 'Contains All',
                             'name': 'contains_all'},
                            {'input_type': 'select_multiple',
                             'label': 'Is Contained By',
                             'name': 'is_contained_by'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares At Least One Element With',
                             'name': 'shares_at_least_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares Exactly One Element With',
                             'name': 'shares_exactly_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares No Elements With',
                             'name': 'shares_no_elements_with'}],
                           'string': [{'input_type': 'text', 'label': 'Contains', 'name': 'contains'},
                            {'input_type': 'text', 'label': 'Ends With', 'name': 'ends_with'},
                            {'input_type': 'text', 'label': 'Equal To', 'name': 'equal_to'},
                            {'input_type': 'text',
                             'label': 'Equal To (case insensitive)',
                             'name': 'equal_to_case_insensitive'},
                            {'input_type': 'text', 'label': 'Matches Regex', 'name': 'matches_regex'},
                            {'input_type': 'none', 'label': 'Non Empty', 'name': 'non_empty'},
                            {'input_type': 'text', 'label': 'Starts With', 'name': 'starts_with'}]})
