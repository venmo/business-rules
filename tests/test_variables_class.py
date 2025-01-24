from business_rules.engine import check_condition
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, rule_variable, boolean_rule_variable
from business_rules.operators import StringType
from unittest import TestCase

class VariablesClassTests(TestCase):
    """ Test methods on classes that inherit from BaseVariables
    """
    def test_base_has_no_variables(self):
        self.assertEqual(len(BaseVariables.get_all_variables()), 0)

    def test_get_all_variables(self):
        """ Returns a dictionary listing all the functions on the class that
        have been decorated as variables, with some of the data about them.
        """
        class SomeVariables(BaseVariables):

            @rule_variable(StringType)
            def this_is_rule_1(self):
                """some docs"""
                return "blah"

            def non_rule(self):
                return "baz"

            @boolean_rule_variable(
                params=[{"fieldType": FIELD_NUMERIC, "name": "x", "label": "X"},
                        {"fieldType": FIELD_NUMERIC, "name": "y", "label": "Y"}]
            )
            def compare(self, x, y):
                return x > y

        vars = SomeVariables.get_all_variables()
        self.assertEqual(len(vars), 2)
        self.assertEqual(vars[1]['name'], 'this_is_rule_1')
        self.assertEqual(vars[1]['label'], 'This Is Rule 1')
        self.assertEqual(vars[1]['field_type'], 'string')
        self.assertEqual(vars[1]['docs'], 'some docs')
        self.assertEqual(vars[1]['options'], [])

        # should work on an instance of the class too
        self.assertEqual(len(SomeVariables().get_all_variables()), 2)

        condition = {
            "name": "compare",
            "operator": "is_true",
            "value": '',
            "params": {"x": 9, "y": 6},
        }
        condition_result = check_condition(condition, SomeVariables())
        self.assertTrue(condition_result)

