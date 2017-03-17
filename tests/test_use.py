from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT
from business_rules import run_all

from . import TestCase

class SomeVariables(BaseVariables):
    @string_rule_variable()
    def foo(self):
        return "foo"

    @numeric_rule_variable(label="ten variable")
    def ten(self):
        return 10


class SomeActions(BaseActions):
    def __init__(self):
        self.calls = []

    @rule_action(params={"some_number": FIELD_NUMERIC})
    def some_number_action(self, some_number):
        self.calls.append({'function': 'some_number_action', 'some_number': some_number})

    @rule_action(label="Some String", params={"some_string": FIELD_TEXT})
    def some_string_action(self, some_string):
        self.calls.append({'function': 'some_string_action', 'some_string': some_string})


class UseCaseTests(TestCase):
    def test_always_true_condition(self):
        rules = [
            {
                'conditions': None,
                'actions': [
                    {'name': 'some_number_action', 'params': {'some_number': 5}},
                ],
            },
        ]

        actions = SomeActions()
        results = run_all(
            rule_list=rules,
            defined_variables=SomeVariables(),
            defined_actions=actions,
            stop_on_first_trigger=False
        )
        self.assertEquals(actions.calls, [{'function': 'some_number_action', 'some_number': 5}])
