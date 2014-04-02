from business_rules import engine
from business_rules.variables import BaseVariables, rule_variable, TYPE_STRING, TYPE_NUMERIC
from business_rules.operators import StringType
from business_rules.actions import BaseActions

from mock import MagicMock
from unittest2 import TestCase


class EngineTests(TestCase):

    ###
    ### Run
    ###

    def test_run_all_some_rule_triggered(self):
        """ By default, does not stop on first triggered rule. Returns True if
        any rule was triggered, otherwise False
        """
        rule1 = {'conditions': 'condition1', 'actions': 'action name 1'}
        rule2 = {'conditions': 'condition2', 'actions': 'action name 2'}
        variables = BaseVariables()
        actions = BaseActions()

        engine.run = MagicMock()
        def return_action1(rule, *args, **kwargs):
            return rule['actions'] == 'action name 1'
        engine.run.side_effect = return_action1

        result = engine.run_all([rule1, rule2], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)

        # switch order and try again
        engine.run = MagicMock()
        engine.run.side_effect = return_action1

        result = engine.run_all([rule2, rule1], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)


    def test_run_all_stop_on_first(self):
        rule1 = {'conditions': 'condition1', 'actions': 'action name 1'}
        rule2 = {'conditions': 'condition2', 'actions': 'action name 2'}
        variables = BaseVariables()
        actions = BaseActions()

        engine.run = MagicMock(return_value=True)
        result = engine.run_all([rule1, rule2], variables, actions,
                stop_on_first_trigger=True)
        self.assertEqual(result, True)
        self.assertEqual(engine.run.call_count, 1)
        engine.run.assert_called_once_with(rule1, variables, actions)

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


    ###
    ### Check conditions
    ###
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

    ###
    ### Operator comparisons
    ###
    def test_check_operator_comparison(self):
        string_type = StringType('yo yo')
        string_type.contains = MagicMock(return_value=True)
        result = engine._do_operator_comparison(string_type, 'contains', 'its mocked')
        self.assertTrue(result)
        string_type.contains.assert_called_once_with('its mocked')


    ###
    ### Actions
    ###
    def test_do_action(self):
        pass
