from unittest import TestCase

from mock import MagicMock, patch

from business_rules import engine
from business_rules.actions import BaseActions
from business_rules.operators import StringType
from business_rules.variables import BaseVariables


class EngineTests(TestCase):

    ###
    ### Run
    ###

    @patch.object(engine, 'run')
    def test_run_all_some_rule_triggered(self, *args):
        """By default, does not stop on first triggered rule. Returns True if
        any rule was triggered, otherwise False
        """
        rule1 = {'conditions': 'condition1', 'actions': 'action name 1'}
        rule2 = {'conditions': 'condition2', 'actions': 'action name 2'}
        variables = BaseVariables()
        actions = BaseActions()

        def return_action1(rule, *args, **kwargs):
            return rule['actions'] == 'action name 1'

        engine.run.side_effect = return_action1

        result = engine.run_all([rule1, rule2], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)

        # switch order and try again
        engine.run.reset_mock()

        result = engine.run_all([rule2, rule1], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)

    @patch.object(engine, 'run', return_value=True)
    def test_run_all_stop_on_first(self, *args):
        rule1 = {'conditions': 'condition1', 'actions': 'action name 1'}
        rule2 = {'conditions': 'condition2', 'actions': 'action name 2'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run_all([rule1, rule2], variables, actions, stop_on_first_trigger=True)
        self.assertEqual(result, True)
        self.assertEqual(engine.run.call_count, 1)
        engine.run.assert_called_once_with(rule1, variables, actions)

    @patch.object(engine, 'check_conditions_recursively', return_value=True)
    @patch.object(engine, 'do_actions')
    def test_run_that_triggers_rule(self, *args):
        rule = {'conditions': 'blah', 'actions': 'blah2'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, True)
        engine.check_conditions_recursively.assert_called_once_with(rule['conditions'], variables)
        engine.do_actions.assert_called_once_with(rule['actions'], actions)

    @patch.object(engine, 'check_conditions_recursively', return_value=False)
    @patch.object(engine, 'do_actions')
    def test_run_that_doesnt_trigger_rule(self, *args):
        rule = {'conditions': 'blah', 'actions': 'blah2'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, False)
        engine.check_conditions_recursively.assert_called_once_with(rule['conditions'], variables)
        self.assertEqual(engine.do_actions.call_count, 0)

    @patch.object(engine, 'check_condition', return_value=True)
    def test_check_all_conditions_with_all_true(self, *args):
        conditions = {'all': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        # assert call count and most recent call are as expected
        self.assertEqual(engine.check_condition.call_count, 2)
        engine.check_condition.assert_called_with({'thing2': ''}, variables)

    ###
    ### Check conditions
    ###
    @patch.object(engine, 'check_condition', return_value=False)
    def test_check_all_conditions_with_all_false(self, *args):
        conditions = {'all': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, False)
        engine.check_condition.assert_called_once_with({'thing1': ''}, variables)

    def test_check_all_condition_with_no_items_fails(self):
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively({'all': []}, BaseVariables())

    @patch.object(engine, 'check_condition', return_value=True)
    def test_check_any_conditions_with_all_true(self, *args):
        conditions = {'any': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        engine.check_condition.assert_called_once_with({'thing1': ''}, variables)

    @patch.object(engine, 'check_condition', return_value=False)
    def test_check_any_conditions_with_all_false(self, *args):
        conditions = {'any': [{'thing1': ''}, {'thing2': ''}]}
        variables = BaseVariables()

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

    @patch.object(engine, 'check_condition')
    def test_nested_all_and_any(self, *args):
        conditions = {'all': [{'any': [{'name': 1}, {'name': 2}]}, {'name': 3}]}
        bv = BaseVariables()

        def side_effect(condition, _):
            return condition['name'] in [2, 3]

        engine.check_condition.side_effect = side_effect

        engine.check_conditions_recursively(conditions, bv)
        self.assertEqual(engine.check_condition.call_count, 3)
        engine.check_condition.assert_any_call({'name': 1}, bv)
        engine.check_condition.assert_any_call({'name': 2}, bv)
        engine.check_condition.assert_any_call({'name': 3}, bv)

    ###
    ### Operator comparisons
    ###
    def test_check_operator_comparison(self):
        string_type = StringType('yo yo')
        with patch.object(string_type, 'contains', return_value=True):
            result = engine._do_operator_comparison(string_type, 'contains', 'its mocked')
            self.assertTrue(result)
            string_type.contains.assert_called_once_with('its mocked')

    ###
    ### Actions
    ###
    def test_do_actions(self):
        actions = [{'name': 'action1'}, {'name': 'action2', 'params': {'param1': 'foo', 'param2': 10}}]
        defined_actions = BaseActions()
        defined_actions.action1 = MagicMock()
        defined_actions.action2 = MagicMock()

        engine.do_actions(actions, defined_actions)

        defined_actions.action1.assert_called_once_with()
        defined_actions.action2.assert_called_once_with(param1='foo', param2=10)

    def test_do_with_invalid_action(self):
        actions = [{'name': 'fakeone'}]
        err_string = "Action fakeone is not defined in class BaseActions"
        with self.assertRaisesRegexp(AssertionError, err_string):
            engine.do_actions(actions, BaseActions())
