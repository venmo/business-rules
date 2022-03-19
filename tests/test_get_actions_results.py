from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, boolean_rule_variable
from business_rules.engine import run_all_with_results
from . import TestCase


class ActionsResultsClassTests(TestCase):
    """ Test methods on getting fired rules actions results
    """
    def test_get_actions_results(self):
        class SomeVariables(BaseVariables):
            @boolean_rule_variable
            def this_is_rule_1(self):
                return True

            @boolean_rule_variable
            def this_is_rule_2(self):
                return False

        class SomeActions(BaseActions):

            @rule_action(params={'foo':FIELD_TEXT})
            def some_action_1(self, foo):
                return foo

            @rule_action(params={'foobar':FIELD_TEXT})
            def some_action_2(self, foobar):
                return foobar

            @rule_action()
            def some_action_3(self):
                pass
        
        rule1 = {'conditions': {'all': [
        {
            'name': 'this_is_rule_1',
            'value': True,
            'operator': 'is_true'
        }]},
        'actions': [
            {'name': 'some_action_1',
            'params': {'foo': 'fooValue'}
            }]}
        rule2 = {'conditions': {'all': [
        {
            'name': 'this_is_rule_2',
            'value': True,
            'operator': 'is_false'
        }]},
        'actions': [
            {'name': 'some_action_2',
            'params': {'foobar': 'foobarValue'}
            },
            {'name': 'some_action_3'
            }]}

        variables = SomeVariables()
        actions = SomeActions()
        result = run_all_with_results([rule1, rule2], variables, actions)
        self.assertEqual(result, [{'some_action_1': 'fooValue'}, {'some_action_2': 'foobarValue'}])
