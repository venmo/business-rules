from business_rules import engine
from business_rules.variables import BaseVariables, rule_variable, TYPE_STRING, TYPE_NUMERIC
from business_rules.operators import StringType
from business_rules.actions import BaseActions

from mock import MagicMock
from unittest2 import TestCase


class EngineTests(TestCase):

    def test_run_that_triggers_rule(self):
        rule = {'conditions': 'blah', 'actions': 'blah2'}
        variables = BaseVariables()
        actions = BaseActions()

        engine.check_conditions_recursively = MagicMock(return_value=True)
        engine.do_actions = MagicMock()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, True)
        engine.check_conditions_recursively.assert_called_once_with(
                rule['conditions'], variables)
        engine.do_actions.assert_called_once_with(rule['actions'], actions)


    def test_run_that_doesnt_trigger_rule(self):
        rule = {'conditions': 'blah', 'actions': 'blah2'}
        variables = BaseVariables()
        actions = BaseActions()

        engine.check_conditions_recursively = MagicMock(return_value=False)
        engine.do_actions = MagicMock()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, False)
        engine.check_conditions_recursively.assert_called_once_with(
                rule['conditions'], variables)
        self.assertEqual(engine.do_actions.call_count, 0)


    def test_check_all_conditions_with_all_true(self):
        conditions = {'all': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        engine.check_condition = MagicMock(return_value=True)

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        # assert call count and most recent call are as expected
        self.assertEqual(engine.check_condition.call_count, 2)
        engine.check_condition.assert_called_with({'thing2': ''}, variables)


    def test_check_all_conditions_with_all_false(self):
        conditions = {'all': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        engine.check_condition = MagicMock(return_value=False)

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, False)
        engine.check_condition.assert_called_once_with({'thing1': ''}, variables)


    def test_check_all_condition_with_no_items_fails(self):
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively({'all': []}, BaseVariables())


    def test_check_any_conditions_with_all_true(self):
        conditions = {'any': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        engine.check_condition = MagicMock(return_value=True)

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        engine.check_condition.assert_called_once_with({'thing1': ''}, variables)


    def test_check_any_conditions_with_all_false(self):
        conditions = {'any': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        engine.check_condition = MagicMock(return_value=False)

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, False)
        # assert call count and most recent call are as expected
        self.assertEqual(engine.check_condition.call_count, 2)
        engine.check_condition.assert_called_with({'thing2': ''}, variables)


    def test_check_any_condition_with_no_items_fails(self):
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively({'any': []}, BaseVariables())


    def test_check_all_and_any_together(self):
        conditions = {'any': [], 'all': []}
        variables = BaseVariables()
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively(conditions, variables)

    def test_check_operator_comparison(self):
        string_type = StringType('yo yo')
        string_type.contains = MagicMock(return_value=True)
        result = engine._do_operator_comparison(string_type, 'contains', 'its mocked')
        self.assertTrue(result)
        string_type.contains.assert_called_once_with('its mocked')



class EngineLogicTests(TestCase):

    def test_all_node(self):
        all_node = { "all": [
      { "name": "10",
        "operator": "equal_to",
        "value": 10,
      },
      { "name": "foo",
        "operator": "contains",
        "value": "o",
      }]}
