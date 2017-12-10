from business_rules import actions, fields


class TestActions(actions.BaseActions):

    @actions.rule_action(params={"param": fields.FIELD_TEXT})
    def example_action(self, param, **kargs):
        pass
