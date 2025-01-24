from business_rules.engine import check_condition
from business_rules import export_rule_data
from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT
from unittest import TestCase


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

    @numeric_rule_variable(
        params=[{"fieldType": FIELD_NUMERIC, "name": "x", "label": "X"},
                {"fieldType": FIELD_NUMERIC, "name": "y", "label": "Y"}]
    )
    def addition(self, x, y):
        return x + y


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
        err_string = 'Variable food or params {} is not defined in class SomeVariables'
        with self.assertRaisesRegex(AssertionError, err_string):
            check_condition(condition, SomeVariables())

    def test_check_incorrect_operator_name(self):
        condition = {'name': 'foo',
                     'operator': 'equal_tooooze',
                     'value': 'foo'}
        with self.assertRaises(AssertionError):
            check_condition(condition, SomeVariables())

    def test_numeric_variable_with_params(self):
        condition = {
            "name": "addition",
            "operator": "equal_to",
            "value": 15,
            "params": {"x": 9, "y": 6},
        }
        condition_result = check_condition(condition, SomeVariables())
        self.assertTrue(condition_result)

    def test_variable_missing_params(self):
        condition = {
            "name": "addition",
            "operator": "equal_to",
            "value": 10,
            "params": {},
        }
        err_string = "addition\(\) missing 2 required positional arguments: 'x' and 'y'"
        with self.assertRaisesRegex(TypeError, err_string):
            check_condition(condition, SomeVariables())

    def test_export_rule_data(self):
        """ Tests that export_rule_data has the three expected keys
        in the right format.
        """
        all_data = export_rule_data(SomeVariables(), SomeActions())
        self.assertEqual(all_data.get("actions"),
                         [{"name": "some_action",
                           "label": "Some Action",
                           "docs": None,
                           "params": [{'fieldType': 'numeric', 'label': 'Foo', 'name': 'foo'}]},
                          {"name": "some_other_action",
                           "label": "woohoo",
                           "docs": None,
                           "params": [{'fieldType': 'text', 'label': 'Bar', 'name': 'bar'}]},
                          {"name": "some_select_action",
                           "label": "Some Select Action",
                           "docs": None,
                           "params": [{'fieldType': FIELD_SELECT,
                                       'name': 'baz',
                                       'label': 'Baz',
                                       'options': [
                                           {'label': 'Chose Me', 'name': 'chose_me'},
                                           {'label': 'Or Me', 'name': 'or_me'}
                                       ]}]
                           }
                          ])
        self.assertEqual(all_data.get("variables"),
                         [{"name": "addition",
                            "label": "Addition",
                            "field_type": "numeric",
                            "options": [],
                            "docs": None,
                            "params": [{'fieldType': 'numeric', 'name': 'x', 'label': 'X'},
                                       {'fieldType': 'numeric', 'name': 'y', 'label': 'Y'}
                                       ]
                          },
                         {"name": "foo",
                           "label": "Foo",
                           "docs": None,
                           "field_type": "string",
                           "options": [],
                           "params": [],
                           },
                          {"name": "ten",
                           "label": "Diez",
                           "docs": None,
                           "field_type": "numeric",
                           "options": [],
                           "params": [],
                           },
                          {'name': 'true_bool',
                           'label': 'True Bool',
                           "docs": None,
                           'field_type': 'boolean',
                           'options': [],
                           "params": [],
                           },
                          ])

        variable_type_operators = all_data.get("variable_type_operators")
        self.assertEqual(variable_type_operators, expected_variable_type_operators)


expected_variable_type_operators = {
    'boolean': [
        {'input_type': 'none', 'label': 'Is False', 'name': 'is_false'},
        {'input_type': 'none', 'label': 'Is True', 'name': 'is_true'}
    ],
    'numeric': [
        {'input_type': 'none', 'label': 'Does Not Exist', 'name': 'does_not_exist'},
        {'input_type': 'numeric', 'label': 'Equal To', 'name': 'equal_to'},
        {'input_type': 'numeric', 'label': 'Greater Than', 'name': 'greater_than'},
        {'input_type': 'numeric', 'label': 'Greater Than Or Equal To', 'name': 'greater_than_or_equal_to'},
        {'input_type': 'numeric', 'label': 'Less Than', 'name': 'less_than'},
        {'input_type': 'numeric', 'label': 'Less Than Or Equal To', 'name': 'less_than_or_equal_to'},
        {'input_type': 'numeric', 'label': 'Not Equal To', 'name': 'not_equal_to'}
    ],
    'select': [
        {'input_type': 'select', 'label': 'Contains', 'name': 'contains'},
        {'input_type': 'select', 'label': 'Contains All', 'name': 'contains_all'},
        {'input_type': 'select', 'label': 'Contains Any', 'name': 'contains_any'},
        {'input_type': 'select', 'label': 'Does Not Contain', 'name': 'does_not_contain'}
    ],
    'select_multiple': [
        {'input_type': 'select_multiple', 'label': 'Compare State With Item (Only for Posting Rule Engine)',
         'name': 'compare_state_with_item'},
        {'input_type': 'select_multiple', 'label': 'Contains All', 'name': 'contains_all'},
        {'input_type': 'select_multiple', 'label': 'Is Contained By', 'name': 'is_contained_by'},
        {'input_type': 'select_multiple', 'label': 'Shares At Least One Element With',
         'name': 'shares_at_least_one_element_with'},
        {'input_type': 'select_multiple', 'label': 'Shares Exactly One Element With',
         'name': 'shares_exactly_one_element_with'},
        {'input_type': 'select_multiple', 'label': 'Shares No Elements With', 'name': 'shares_no_elements_with'}
    ],
    'string': [
        {'input_type': 'text', 'label': 'Contains', 'name': 'contains'},
        {'input_type': 'text', 'label': 'Contains (case insensitive)', 'name': 'contains_case_insensitive'},
        {'input_type': 'text', 'label': 'Does Not Contain', 'name': 'does_not_contain'},
        {'input_type': 'text', 'label': 'Does not contain (case insensitive)',
         'name': 'does_not_contain_case_insensitive'},
        {'input_type': 'text', 'label': 'Does Not End With', 'name': 'does_not_end_with'},
        {'input_type': 'text', 'label': 'Does Not Match Regex', 'name': 'does_not_match_regex'},
        {'input_type': 'text', 'label': 'Does Not Start With', 'name': 'does_not_start_with'},
        {'input_type': 'text', 'label': 'Ends With', 'name': 'ends_with'},
        {'input_type': 'text', 'label': 'Equal To', 'name': 'equal_to'},
        {'input_type': 'text', 'label': 'Equal To (case insensitive)', 'name': 'equal_to_case_insensitive'},
        {'input_type': 'none', 'label': 'Is Empty', 'name': 'is_empty'},
        {'input_type': 'text', 'label': 'Matches Regex', 'name': 'matches_regex'},
        {'input_type': 'none', 'label': 'Non Empty', 'name': 'non_empty'},
        {'input_type': 'text', 'label': 'Not Equal To', 'name': 'not_equal_to'},
        {'input_type': 'text', 'label': 'Not equal To (case insensitive)', 'name': 'not_equal_to_case_insensitive'},
        {'input_type': 'text', 'label': 'Starts With', 'name': 'starts_with'}
    ]
}
