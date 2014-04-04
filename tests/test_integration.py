from business_rules.engine import check_condition, export_rule_data
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC

from . import TestCase

class SomeVariables(BaseVariables):

    @string_rule_variable()
    def foo(self):
        return "foo"

    @numeric_rule_variable(label="Diez")
    def ten(self):
        return 10

class SomeActions(BaseActions):

    @rule_action(params={"foo": FIELD_NUMERIC})
    def some_action(self, foo): pass

    @rule_action(label="woohoo", params={"bar": FIELD_TEXT})
    def some_other_action(self, bar): pass


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
                           "options": []}])
