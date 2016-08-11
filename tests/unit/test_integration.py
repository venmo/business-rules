from business_rules.engine import check_condition
from business_rules import export_rule_data
from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT

from tests import TestCase

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

        print all_data.get("variable_type_operators")
        self.assertEqual(all_data.get("variable_type_operators"),
                         {
                             'select_multiple': [{
                                 'input_type': 'select_multiple',
                                 'name': 'contains_all',
                                 'label': 'Contains All'
                             }, {
                                 'input_type': 'select_multiple',
                                 'name': 'is_contained_by',
                                 'label': 'Is Contained By'
                             }, {
                                 'input_type': 'select_multiple',
                                 'name': 'shares_at_least_one_element_with',
                                 'label': 'Shares At Least One Element With'
                             }, {
                                 'input_type': 'select_multiple',
                                 'name': 'shares_exactly_one_element_with',
                                 'label': 'Shares Exactly One Element With'
                             }, {
                                 'input_type': 'select_multiple',
                                 'name': 'shares_no_elements_with',
                                 'label': 'Shares No Elements With'
                             }],
                             'string': [{
                                 'input_type': 'text',
                                 'name': 'contains',
                                 'label': 'Contains'
                             }, {
                                 'input_type': 'text',
                                 'name': 'ends_with',
                                 'label': 'Ends With'
                             }, {
                                 'input_type': 'text',
                                 'name': 'equal_to',
                                 'label': 'Equal To'
                             }, {
                                 'input_type': 'text',
                                 'name': 'equal_to_case_insensitive',
                                 'label': 'Equal To (case insensitive)'
                             }, {
                                 'input_type': 'text',
                                 'name': 'matches_regex',
                                 'label': 'Matches Regex'
                             }, {
                                 'input_type': 'none',
                                 'name': 'non_empty',
                                 'label': 'Non Empty'
                             }, {
                                 'input_type': 'text',
                                 'name': 'starts_with',
                                 'label': 'Starts With'
                             }],
                             'numeric': [{
                                 'input_type': 'numeric',
                                 'name': 'equal_to',
                                 'label': 'Equal To'
                             }, {
                                 'input_type': 'numeric',
                                 'name': 'greater_than',
                                 'label': 'Greater Than'
                             }, {
                                 'input_type': 'numeric',
                                 'name': 'greater_than_or_equal_to',
                                 'label': 'Greater Than Or Equal To'
                             }, {
                                 'input_type': 'numeric',
                                 'name': 'less_than',
                                 'label': 'Less Than'
                             }, {
                                 'input_type': 'numeric',
                                 'name': 'less_than_or_equal_to',
                                 'label': 'Less Than Or Equal To'
                             }],
                             'boolean': [{
                                 'input_type': 'none',
                                 'name': 'is_false',
                                 'label': 'Is False'
                             }, {
                                 'input_type': 'none',
                                 'name': 'is_true',
                                 'label': 'Is True'
                             }],
                             'custom_operator': [],
                             'select': [{
                                 'input_type': 'select',
                                 'name': 'contains',
                                 'label': 'Contains'
                             }, {
                                 'input_type': 'select',
                                 'name': 'does_not_contain',
                                 'label': 'Does Not Contain'
                             }]
                         })
