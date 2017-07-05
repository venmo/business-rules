from business_rules.actions import rule_action, BaseActions
from business_rules.engine import check_condition, run_all
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
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

    @numeric_rule_variable(params=[{'field_type': FIELD_NUMERIC, 'name': 'x', 'label': 'X'}])
    def x_plus_one(self, x):
        return x + 1

    @boolean_rule_variable()
    def rule_received(self, **kwargs):
        rule = kwargs.get('rule')
        assert rule is not None
        return rule is not None

    @string_rule_variable(label="StringLabel", options=['one', 'two', 'three'])
    def string_variable_with_options(self):
        return "foo"

    @string_rule_variable(public=False)
    def private_string_variable(self):
        return 'foo'


class SomeActions(BaseActions):
    @rule_action(params={"foo": FIELD_NUMERIC})
    def some_action(self, foo): pass

    @rule_action(label="woohoo", params={"bar": FIELD_TEXT})
    def some_other_action(self, bar): pass

    @rule_action(params=[
        {
            'fieldType': FIELD_SELECT,
            'name': 'baz',
            'label': 'Baz',
            'options': [
                {'label': 'Chose Me', 'name': 'chose_me'},
                {'label': 'Or Me', 'name': 'or_me'}
            ]
        }])
    def some_select_action(self, baz): pass

    @rule_action()
    def action_with_no_params(self): pass


class IntegrationTests(TestCase):
    """ Integration test, using the library like a user would.
    """

    def test_true_boolean_variable(self):
        condition = {
            'name': 'true_bool',
            'operator': 'is_true',
            'value': ''
        }

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertTrue(condition_result.result)

    def test_false_boolean_variable(self):
        condition = {
            'name': 'true_bool',
            'operator': 'is_false',
            'value': ''
        }

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertFalse(condition_result.result)

    def test_check_true_condition_happy_path(self):
        condition = {'name': 'foo',
                     'operator': 'contains',
                     'value': 'o'}

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertTrue(condition_result.result)

    def test_check_false_condition_happy_path(self):
        condition = {'name': 'foo',
                     'operator': 'contains',
                     'value': 'm'}

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertFalse(condition_result.result)

    def test_numeric_variable_with_params(self):
        condition = {
            'name': 'x_plus_one',
            'operator': 'equal_to',
            'value': 10,
            'params': {'x': 9}
        }

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)

        self.assertTrue(condition_result.result)

    def test_check_incorrect_method_name(self):
        condition = {
            'name': 'food',
            'operator': 'equal_to',
            'value': 'm'
        }

        rule = {
            'conditions': condition
        }

        err_string = 'Variable food is not defined in class SomeVariables'

        with self.assertRaisesRegexp(AssertionError, err_string):
            check_condition(condition, SomeVariables(), rule)

    def test_check_incorrect_operator_name(self):
        condition = {
            'name': 'foo',
            'operator': 'equal_tooooze',
            'value': 'foo'
        }

        rule = {
            'conditions': condition
        }

        with self.assertRaises(AssertionError):
            check_condition(condition, SomeVariables(), rule)

    def test_check_missing_params(self):
        condition = {
            'name': 'x_plus_one',
            'operator': 'equal_to',
            'value': 10,
            'params': {}
        }

        rule = {
            'conditions': condition
        }

        err_string = 'Missing parameters x for variable x_plus_one'

        with self.assertRaisesRegexp(AssertionError, err_string):
            check_condition(condition, SomeVariables(), rule)

    def test_check_invalid_params(self):
        condition = {
            'name': 'x_plus_one',
            'operator': 'equal_to',
            'value': 10,
            'params': {'x': 9, 'y': 9}
        }

        rule = {
            'conditions': condition
        }

        err_string = 'Invalid parameters y for variable x_plus_one'

        with self.assertRaisesRegexp(AssertionError, err_string):
            check_condition(condition, SomeVariables(), rule)

    def test_variable_received_rules(self):
        condition = {
            'name': 'rule_received',
            'operator': 'is_true',
            'value': 'true',
        }

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertTrue(condition_result)

    def test_string_variable_with_options_with_wrong_value(self):
        condition = {
            'name': 'string_variable_with_options',
            'operator': 'equal_to',
            'value': 'foo',
        }

        rule = {
            'conditions': condition
        }

        condition_result = check_condition(condition, SomeVariables(), rule)
        self.assertTrue(condition_result)

    def test_run_with_no_conditions(self):
        actions = [
            {
                'name': 'action_with_no_params'
            }
        ]

        rule = {
            'actions': actions
        }

        result = run_all(rule_list=[rule], defined_variables=SomeVariables(), defined_actions=SomeActions())

        self.assertTrue(result)
