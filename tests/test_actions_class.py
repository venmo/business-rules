from business_rules.actions import BaseActions, rule_action
from unittest import TestCase

class ActionsClassTests(TestCase):
    """ Test methods on classes that inherit from BaseActions.
    """
    def test_base_has_no_actions(self):
        self.assertEqual(len(BaseActions.get_all_actions()), 0)

    def test_get_all_actions(self):
        """ Returns a dictionary listing all the functions on the class that
        have been decorated as actions, with some of the data about them.
        """
        class SomeActions(BaseActions):

            @rule_action(params={'foo':'text'})
            def some_action(self):
                return "blah"

            def non_action(self):
                return "baz"

        actions = SomeActions.get_all_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]['name'], 'some_action')
        self.assertEqual(actions[0]['description'], 'Some Action')
        self.assertEqual(actions[0]['params'], {'foo': 'text'})

        # should work on an instance of the class too
        self.assertEqual(len(SomeActions().get_all_actions()), 1)
