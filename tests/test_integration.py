from business_rules.engine import check_condition
from business_rules import export_rule_data
from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC

from . import TestCase

class SomeVariables(BaseVariables):

    @string_rule_variable()
    def foo(self):
        return "foo"

    @numeric_rule_variable(label="Diez")
    def ten(self):
        return 10

    @boolean_rule_variable()
    def true_bool(self):
        return True

class SomeActions(BaseActions):

    @rule_action(params={"foo": FIELD_NUMERIC})
    def some_action(self, foo): pass

    @rule_action(label="woohoo", params={"bar": FIELD_TEXT})
    def some_other_action(self, bar): pass


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
                  "params": {"foo":"numeric"}},
                 {"name": "some_other_action",
                  "label": "woohoo",
                  "params": {"bar":"text"}}])

        self.assertEqual(all_data.get("variables"),
                         [{"name": "foo",
                           "label": "Foo",
                           "field_type": "string",
                           "options": []},
                          {"name": "ten",
                           "label": "Diez",
                           "field_type": "numeric",
                           "options": []},
                          {'name': 'true_bool',
                           'label': 'True Bool',
                           'field_type': 'boolean',
                           'options': []}])

        self.assertEqual(all_data.get("variable_type_operators"),
                         {'boolean': [{'input_type': 'none',
                             'label': 'Is False',
                             'name': 'is_false'},
                            {'input_type': 'none',
                             'label': 'Is True',
                             'name': 'is_true'}],
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
