from business_rules.variables import BaseVariables, rule_variable
from business_rules.operators import StringType
from business_rules.fields import FIELD_TEXT
from . import TestCase

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

            @rule_variable(StringType, params=[{'field_type': FIELD_TEXT, 'name': 'foo', 'label': 'Foo'}])
            def this_is_rule_1(self, foo):
                return "blah"

            def non_rule(self):
                return "baz"

        vars = SomeVariables.get_all_variables()
        self.assertEqual(len(vars), 1)
        self.assertEqual(vars[0]['name'], 'this_is_rule_1')
        self.assertEqual(vars[0]['label'], 'This Is Rule 1')
        self.assertEqual(vars[0]['field_type'], 'string')
        self.assertEqual(vars[0]['options'], [])
        self.assertEqual(vars[0]['params'], [{'field_type': FIELD_TEXT, 'name': 'foo', 'label': 'Foo'}])

        # should work on an instance of the class too
        self.assertEqual(len(SomeVariables().get_all_variables()), 1)

